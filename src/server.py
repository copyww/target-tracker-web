from fastapi import FastAPI,UploadFile,Form
from fastapi.responses import JSONResponse
import os


app = FastAPI()

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

@app.post("/upload/")
#async 异步
async def upload_file(file: UploadFile, user: str =Form("user1") ):
    user_dir = os.path.join(UPLOADS_DIR, user)
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return JSONResponse(content={
        "filename": file.filename,
        "user": user,
        "message": "File uploaded successfully"
    })