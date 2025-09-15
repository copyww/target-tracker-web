# db.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from datetime import datetime
# from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select


from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 用户表
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    videos = relationship("Video", back_populates="user")

# 视频表
class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    path = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="videos")

# 创建数据库引擎和 Session
DATABASE_URL = "sqlite+aiosqlite:///./app.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine,class_=AsyncSession, expire_on_commit=False)
