from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class VideoData(BaseModel):
    id: Optional[int] = 1
    title: str
    description: str
    publishing_datetime: datetime
    thumbnail_urls: str
    video_url: str