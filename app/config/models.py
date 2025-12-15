from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import List, Union

class DataParent(BaseModel):
    views_count: int
    likes_count: int
    comments_count: int
    reports_count: int
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def to_datetime(data_of_datetime: Union[str, datetime]) -> datetime:
        if isinstance(data_of_datetime, str):
            return datetime.fromisoformat(data_of_datetime)
        return data_of_datetime

    @field_validator('created_at', mode='before')
    def validate_created_at(cls, data):
        return cls.to_datetime(data)

    @field_validator('updated_at', mode='before')
    def validate_updated_at(cls, data):
        return cls.to_datetime(data)

class SnapshotsModel(DataParent):
    id: str
    video_id: str
    delta_views_count: int
    delta_likes_count: int
    delta_comments_count: int
    delta_reports_count: int


class VideosModel(DataParent):
    id: str
    creator_id: str
    video_created_at: datetime
    snapshots: Union[List[SnapshotsModel], None] = Field(exclude=True, default=None)

    @field_validator('video_created_at', mode='before')
    def validate_video_created_at(cls, data):
        return cls.to_datetime(data)

class Video(BaseModel):
    videos: List[VideosModel]
