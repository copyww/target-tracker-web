from fastapi import FastAPI,UploadFile,Form
from fastapi.responses import JSONResponse
import os
from sqlalchemy.orm import Session
from db import SessionLocal, User, Video, select
import shutil


app = FastAPI()

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

@app.post("/upload/")
#async 异步
async def upload_file(file: UploadFile, user: str =Form("user1") ):
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