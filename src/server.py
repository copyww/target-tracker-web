from fastapi import FastAPI, HTTPException, UploadFile, Header
from fastapi.responses import FileResponse, JSONResponse
import os
from sqlalchemy.orm import Session
from db import SessionLocal, User, Video, select
from pydantic import BaseModel
import cv2
from urllib.parse import quote
import uuid
import subprocess

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

# UPLOADS_DIR = "uploads"
# os.makedirs(UPLOADS_DIR, exist_ok=True)

from fastapi.staticfiles import StaticFiles
THUMBNAILS_DIR = "thumbnails"
os.makedirs(THUMBNAILS_DIR, exist_ok=True)


HLS_DIR = "hls"
os.makedirs(HLS_DIR, exist_ok=True)
app.mount("/thumbnails", StaticFiles(directory=THUMBNAILS_DIR), name="thumbnails")


#获取视频文件来播放，把视频文件夹挂载 用hls
# app.mount("/hls", StaticFiles(directory=HLS_DIR), name="hls")


@app.post("/upload/")
async def upload_file(file: UploadFile, user: str = Header("user1", alias="Username")):
    # ========= 保存原始上传文件到临时目录 =========
    tmp_dir = os.path.join("tmp_uploads", user)
    os.makedirs(tmp_dir, exist_ok=True)
    safe_filename = sanitize_filename(file.filename)
    tmp_file_path = os.path.join(tmp_dir, safe_filename)
    with open(tmp_file_path, "wb") as f:
        f.write(await file.read())

    # ========= 生成缩略图 =========
    user_thumb_dir = os.path.join(THUMBNAILS_DIR, user)
    os.makedirs(user_thumb_dir, exist_ok=True)
    thumbnail_filename = f"{os.path.splitext(safe_filename)[0]}_thumb.jpg"
    thumbnail_path = os.path.join(user_thumb_dir, thumbnail_filename)
    generate_thumbnail(tmp_file_path, thumbnail_path)

    # ========= 转 HLS =========
    hls_basename = os.path.splitext(safe_filename)[0]
    hls_user_dir = os.path.join(HLS_DIR, user, hls_basename)
    os.makedirs(hls_user_dir, exist_ok=True)
    hls_path = os.path.join(hls_user_dir, f"{hls_basename}.m3u8")

    ffmpeg = r"F:\环境\ffmpeg-2025-09-15-git-16b8a7805b-essentials_build\bin\ffmpeg.exe"
    subprocess.run([
        ffmpeg,
        "-i", tmp_file_path,
        "-codec:", "copy",
        "-start_number", "0",
        "-hls_time", "10",
        "-hls_list_size", "0",
        "-f", "hls",
        hls_path
    ], check=True)

    # ========= 删除原始 MP4 =========
    os.remove(tmp_file_path)

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
            title=file.filename,
            path=f"/hls/{user}/{hls_basename}/{hls_basename}.m3u8",
            thumbnail=f"/thumbnails/{user}/{thumbnail_filename}",
            user_id=db_user.id
        )
        session.add(new_video)
        await session.commit()

    return JSONResponse(content={
        "filename": file.filename,
        "thumbnail": f"/thumbnails/{user}/{quote(thumbnail_filename)}",
        "hls_path": f"/hls/{user}/{hls_basename}/{hls_basename}.m3u8",
        "user": user,
        "message": "File uploaded and converted to HLS successfully"
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
                "path": f"http://127.0.0.1:8000{video.path.replace(os.sep, '/')}",
                "upload_time": video.upload_time,
                "thumbnail": f"http://127.0.0.1:8000{os.path.dirname(video.thumbnail)}/{quote(os.path.basename(video.thumbnail))}"
            }
            for video in videos
        ]






@app.get("/hls/{user}/{video_id}/{filename}")
@app.head("/hls/{user}/{video_id}/{filename}")  
async def get_hls(user: str, video_id: str, filename: str):
    """
    提供 HLS 播放文件（m3u8 + ts 切片）
    - user: 用户名 (user1)
    - video_id: 视频唯一id
    - filename: 具体文件名 (m3u8 或 ts)
    """
    file_path = os.path.join(HLS_DIR, user, video_id, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # 根据文件后缀返回正确类型
    if filename.endswith(".m3u8"):
        media_type = "application/vnd.apple.mpegurl"
    elif filename.endswith(".ts"):
        media_type = "video/mp2t"
    else:
        media_type = "application/octet-stream"

    return FileResponse(file_path, media_type=media_type)