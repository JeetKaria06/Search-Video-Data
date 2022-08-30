import logging
import os
from typing import List
from datetime import datetime
from googleapiclient.discovery import build

from src.models import VideoData
from src.db import write_query

API_KEY = os.environ["YT_API_KEY"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

logger = logging.getLogger("__name__")

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
next_page_token = "something"

async def fetch_and_add_video_data():
    video_data_list: List[VideoData] = await search("cricket")
    await write_query(video_data_list=video_data_list)


async def search(search_query: str) -> List[VideoData]:
    global next_page_token

    if next_page_token == "something":
        search_response = youtube.search().list(
            q=search_query,
            part='id,snippet',
            type='video',
            order='date',
            publishedAfter="2022-01-01T00:00:00Z",
            maxResults=20,
        ).execute()
    elif next_page_token != "":
        search_response = youtube.search().list(
            q=search_query,
            part='id,snippet',
            type='video',
            order='date',
            publishedAfter="2022-01-01T00:00:00Z",
            maxResults=20,
            pageToken=next_page_token
        ).execute()
    else:
        pass

    video_data_list: List[VideoData] = []
    for item in search_response["items"]:
        video_data = VideoData(
            description=item["snippet"]["description"],
            title=item["snippet"]["title"],
            publishing_datetime=datetime.strptime(item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
            thumbnail_urls=f'{item["snippet"]["thumbnails"]["default"]["url"]},{item["snippet"]["thumbnails"]["medium"]["url"]},{item["snippet"]["thumbnails"]["high"]["url"]}',
            video_url=f'https://youtube.com/watch?v={item["id"]["videoId"]}',
        )

        video_data_list.append(video_data)

    next_page_token = search_response.get("nextPageToken", "")

    return video_data_list