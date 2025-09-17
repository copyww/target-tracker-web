# init_db.py
from db import Base, engine, User, Video,SessionLocal,select

import asyncio

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())

# 添加默认用户 usr1
from sqlalchemy.orm import Session



async def add_default_user():
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(username="usr1"))
        user = result.scalars().first()
        if not user:
            session.add(User(username="usr1"))
            await session.commit()

asyncio.run(add_default_user())


