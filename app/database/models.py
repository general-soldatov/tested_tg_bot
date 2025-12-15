from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Videos(Base):
    __tablename__ = 'videos'
    id = Column(String, primary_key=True)
    creator_id = Column(String, unique=True)
    video_created_at = Column(DateTime)
    views_count = Column(Integer)
    likes_count = Column(Integer)
    comments_count = Column(Integer)
    reports_count = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Snapshots(Base):
    __tablename__ = "video_snapshots"
    id = Column(String, primary_key=True)
    video_id = Column(String)
    views_count = Column(Integer)
    likes_count = Column(Integer)
    comments_count = Column(Integer)
    reports_count = Column(Integer)
    delta_views_count = Column(Integer)
    delta_likes_count = Column(Integer)
    delta_comments_count = Column(Integer)
    delta_reports_count = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
