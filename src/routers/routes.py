from fastapi import APIRouter, Body
from fastapi_pagination import Page, paginate

from src.models import VideoData
from src.db import get_query, search_query

router = APIRouter()

@router.get("/fetch-video-data", response_model=Page[VideoData])
async def fetch_video_data():
    result = await get_query()
    video_data_list = [
        VideoData(
            id=item.id,
            title=item.title,
            description=item.description,
            publishing_datetime=item.publishing_datetime,
            thumbnail_urls=item.thumbnail_urls,
            video_url=item.video_url,
        ) for item in result
    ]
    return paginate(video_data_list)


@router.post("/search-video-data", response_model=Page[VideoData])
async def search_video_data(search_string: str = Body("Search String")):
    result = await search_query(search_string=search_string)
    video_data_list = [
        VideoData(
            id=item.id,
            title=item.title,
            description=item.description,
            publishing_datetime=item.publishing_datetime,
            thumbnail_urls=item.thumbnail_urls,
            video_url=item.video_url,
        ) for item in result
    ]
    return paginate(video_data_list)