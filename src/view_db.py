import asyncio
from db import SessionLocal, User, Video, select

async def view_db():
    async with SessionLocal() as session:
        # 查看所有用户
        result = await session.execute(select(User))
        users = result.scalars().all()
        print("Users in database:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Password: {user.password}")

        # 查看所有视频
        result = await session.execute(select(Video))
        videos = result.scalars().all()
        print("\nVideos in database:")
        for video in videos:
            print(f"ID: {video.id}, Title: {video.title}, Path: {video.path}, Upload_time: {video.upload_time}, User_id: {video.user_id}")

asyncio.run(view_db())
