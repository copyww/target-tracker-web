from fastapi import FastAPI, UploadFile, Header
from fastapi.responses import JSONResponse
import os
from sqlalchemy.orm import Session
from db import SessionLocal, User, Video, select
from pydantic import BaseModel
import cv2
from urllib.parse import quote
import uuid

def generate_thumbnail(video_path, thumbnail_path):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    if success:
        cv2.imwrite(thumbnail_path, frame)
    cap.release()

def sanitize_filename(filename):
    ext = os.path.splitext(filename)[1]  # 保留原始扩展名
    new_name = f"{uuid.uuid4().hex}{ext}"
    return new_name


app = FastAPI()

# 允许的前端地址
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

from fastapi.staticfiles import StaticFiles
THUMBNAILS_DIR = "thumbnails"
os.makedirs(THUMBNAILS_DIR, exist_ok=True)
app.mount("/thumbnails", StaticFiles(directory=THUMBNAILS_DIR), name="thumbnails")


@app.post("/upload/")
async def upload_file(file: UploadFile, user: str = Header("user1", alias="Username")):
    # ========= 保存视频 =========
    user_video_dir = os.path.join(UPLOADS_DIR, user)
    os.makedirs(user_video_dir, exist_ok=True)
    safe_filename = sanitize_filename(file.filename)  # ✅ 使用 sanitize
    file_path = os.path.join(user_video_dir, safe_filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # ========= 保存缩略图 =========
    user_thumb_dir = os.path.join(THUMBNAILS_DIR, user)
    os.makedirs(user_thumb_dir, exist_ok=True)
    thumbnail_filename = f"{os.path.splitext(safe_filename)[0]}_thumb.jpg"  # ✅ 使用 sanitize 后的 safe_filename
    thumbnail_path = os.path.join(user_thumb_dir, thumbnail_filename)
    generate_thumbnail(file_path, thumbnail_path)

    # ========= 保存数据库 =========
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(username=user))
        db_user = result.scalars().first()
        if not db_user:
            db_user = User(username=user)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)

        new_video = Video(
            title=file.filename,  # 原始中文名保存到数据库
            path=file_path,
            thumbnail=f"/thumbnails/{user}/{thumbnail_filename}",
            user_id=db_user.id
        )
        session.add(new_video)
        await session.commit()

    return JSONResponse(content={
        "filename": file.filename,
        "thumbnail": f"/thumbnails/{user}/{quote(thumbnail_filename)}",
        "user": user,
        "message": "File uploaded successfully"
    })


class UsernameRequest(BaseModel):
    username: str


@app.post("/videos/")
async def get_videos_for_user(data: UsernameRequest):
    username = data.username
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(username=username))
        user = result.scalars().first()
        if not user:
            return []

        result = await session.execute(select(Video).filter_by(user_id=user.id))
        videos = result.scalars().all()

        return [
            {
                "id": video.id,
                "title": video.title,
                "path": video.path,
                "upload_time": video.upload_time,
                "thumbnail": f"http://127.0.0.1:8000{os.path.dirname(video.thumbnail)}/{quote(os.path.basename(video.thumbnail))}"
            }
            for video in videos
        ]
