import asyncio
from db import Base, engine

async def reset_db():
    async with engine.begin() as conn:
        # 删除所有表
        await conn.run_sync(Base.metadata.drop_all)
        # 重新创建表
        await conn.run_sync(Base.metadata.create_all)
    print("数据库表已清空并重建。")

if __name__ == "__main__":
    asyncio.run(reset_db())
