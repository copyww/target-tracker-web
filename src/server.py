import json
from fastapi import FastAPI, HTTPException, UploadFile, Header, WebSocket, WebSocketDisconnect
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
app.mount("/tmp_uploads", StaticFiles(directory="tmp_uploads"), name="tmp_uploads")


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
            path=f"/hls/{user}/{hls_basename}/{hls_basename}.m3u8",  # HLS 路径
            mp4_path=f"/tmp_uploads/{user}/{safe_filename}",          # 原始 MP4 路径
            thumbnail=f"/thumbnails/{user}/{thumbnail_filename}",
            user_id=db_user.id
        )
        session.add(new_video)
        await session.commit()

    return JSONResponse(content={
        "filename": file.filename,
        "thumbnail": f"/thumbnails/{user}/{quote(thumbnail_filename)}",
        "hls_path": f"/hls/{user}/{hls_basename}/{hls_basename}.m3u8",
        "mp4_path": f"/tmp_uploads/{user}/{quote(safe_filename)}",
        "user": user,
        "message": "File uploaded, MP4 saved, and converted to HLS successfully"
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

        base_url = "http://127.0.0.1:8000"

        return [
            {
                "id": video.id,
                "title": video.title,
                "hls_path": f"{base_url}{video.path.replace(os.sep, '/')}",
                "mp4_path": f"{base_url}{video.mp4_path.replace(os.sep, '/')}" if getattr(video, "mp4_path", None) else None,
                "upload_time": video.upload_time,
                "thumbnail": f"{base_url}{video.thumbnail.replace(os.sep, '/')}"
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


from HybridTracker import HybridTracker

tracker = None
video_cap = None
current_video_path = None

# 保存初始模板
roi_template = None
roi_size = None
roi_saved_frame = None


def template_match_search(frame, template, search_region=None, threshold=0.6):
    """基于模板匹配重新检测目标"""
    if template is None:
        return None, 0.0

    if search_region is not None:
        x, y, w, h = search_region
        frame_crop = frame[y:y + h, x:x + w]
        search_offset = (x, y)
    else:
        frame_crop = frame
        search_offset = (0, 0)

    res = cv2.matchTemplate(frame_crop, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val < threshold:
        return None, max_val

    top_left = (max_loc[0] + search_offset[0], max_loc[1] + search_offset[1])
    w, h = template.shape[1], template.shape[0]
    return (top_left[0], top_left[1], w, h), max_val


@app.websocket("/ws/track")
async def websocket_endpoint(websocket: WebSocket):
    global tracker, video_cap, current_video_path, roi_template, roi_size, roi_saved_frame
    await websocket.accept()
    print("✅ WebSocket 连接成功")

    try:
        while True:
            data = await websocket.receive_text()
            frame_info = json.loads(data)
            msg_type = frame_info.get("type")
            mp4_path = frame_info.get("mp4_path")

            if not mp4_path:
                await websocket.send_text(json.dumps({"error": "mp4_path missing"}))
                continue

            # 切换视频时重置
            if current_video_path != mp4_path:
                if video_cap:
                    video_cap.release()
                local_path = mp4_path.replace("http://127.0.0.1:8000", ".")
                video_cap = cv2.VideoCapture(local_path)
                current_video_path = mp4_path
                tracker = HybridTracker()
                roi_template = None
                roi_size = None
                roi_saved_frame = None
                print(f"📌 切换新视频: {mp4_path}")

            # 定位帧
            video_cap.set(cv2.CAP_PROP_POS_MSEC, frame_info["time"] * 1000)
            ret, frame = video_cap.read()
            if not ret or frame is None:
                await websocket.send_text(json.dumps({"error": "cannot read frame"}))
                continue

            # 初始化 ROI
            if msg_type == "init" and "roi" in frame_info:
                roi = frame_info["roi"]
                x, y, w, h = int(roi["x"]), int(roi["y"]), int(roi["width"]), int(roi["height"])

                frame_h, frame_w = frame.shape[:2]
                x = max(0, x)
                y = max(0, y)
                w = min(w, frame_w - x)
                h = min(h, frame_h - y)

                if w <= 0 or h <= 0:
                    await websocket.send_text(json.dumps({"error": "invalid ROI bbox"}))
                    continue

                bbox = (x, y, w, h)
                tracker = HybridTracker()
                tracker.initialize_tracker(frame, bbox)

                # 保存初始模板
                roi_template = frame[y:y + h, x:x + w].copy()
                roi_size = (w, h)
                roi_saved_frame = frame.copy()

                os.makedirs("debug_frames", exist_ok=True)
                debug_path = os.path.join("debug_frames", "first_roi.png")
                cv2.imwrite(debug_path, roi_saved_frame)
                print(f"✅ 保存第一帧 ROI 模板 {debug_path}")

            # 更新追踪
            success, bbox = tracker.update(frame)

            # 如果失败，尝试模板匹配恢复
            if not success and roi_template is not None:
                # 只在上一帧位置附近扩大 2 倍范围搜索
                search_region = None
                if bbox is not None:
                    x, y, w, h = map(int, bbox)
                    search_region = (
                        max(0, x - w),
                        max(0, y - h),
                        min(3 * w, frame.shape[1] - x + w),
                        min(3 * h, frame.shape[0] - y + h),
                    )
                new_bbox, score = template_match_search(frame, roi_template, search_region, threshold=0.55)
                if new_bbox:
                    tracker.initialize_tracker(frame, new_bbox)
                    bbox = new_bbox
                    success = True
                    print(f"🔄 模板匹配恢复成功，相似度 {score:.2f}")
                    # 保存调试图
                    debug_path = os.path.join("debug_frames", "recovery.png")
                    frame_debug = frame.copy()
                    x, y, w, h = map(int, bbox)
                    cv2.rectangle(frame_debug, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.imwrite(debug_path, frame_debug)

            # 返回结果
            if success and bbox is not None:
                x, y, w, h = map(int, bbox)
                return_box = {"x": x, "y": y, "width": w, "height": h}
            else:
                return_box = {"x": 0, "y": 0, "width": 0, "height": 0}

            await websocket.send_text(json.dumps(return_box))

    except WebSocketDisconnect:
        print("❌ 客户端断开连接")
    finally:
        if video_cap:
            video_cap.release()
            video_cap = None
            current_video_path = None