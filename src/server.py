from fastapi import FastAPI,UploadFile,Header,Body
from fastapi.responses import JSONResponse
import os
from sqlalchemy.orm import Session
from db import SessionLocal, User, Video, select
import shutil
from pydantic import BaseModel


app = FastAPI()


# 允许的前端地址
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

@app.post("/upload/")
#async 异步
async def upload_file(file: UploadFile, user: str = Header("user1",alias="Username") ):
    # 保存上传的文件
    user_dir = os.path.join(UPLOADS_DIR, user)
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 保存文件信息到数据库 异步
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(username=user))
        db_user = result.scalars().first()
        if not db_user:
            db_user = User(username=user)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
        
        new_video = Video(title=file.filename, path=file_path, user_id=db_user.id)
        session.add(new_video)
        await session.commit()

    return JSONResponse(content={
        "filename": file.filename,
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
        return [{"id": video.id, "title": video.title, "path": video.path, "upload_time": video.upload_time} for video in videos]