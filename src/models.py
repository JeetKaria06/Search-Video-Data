from pydantic import BaseModel
from datetime import datetime

class VideoData(BaseModel):
    id: int
    title: str
    description: str
    publishing_datetime: datetime
    thumbnail_urls: str
    video_url: str