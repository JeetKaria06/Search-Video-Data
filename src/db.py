import os
from typing import List
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, or_
from sqlalchemy.future import select

from src.models import VideoData as VideoDataModel

MYSQL_USERNAME = os.environ["MYSQL_USERNAME"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_HOSTNAME = os.environ["MYSQL_HOSTNAME"]
MYSQL_PORT = os.environ["MYSQL_PORT"]
MYSQL_DBNAME = os.environ["MYSQL_DBNAME"]
POOL_SIZE = int(os.environ["POOL_SIZE"])
MYSQL_TABLENAME = os.environ["MYSQL_TABLENAME"]

db_connection_string = f"mysql+aiomysql://{MYSQL_USERNAME}:{quote_plus(MYSQL_PASSWORD)}@{MYSQL_HOSTNAME}:{MYSQL_PORT}/{MYSQL_DBNAME}"

engine = create_async_engine(db_connection_string, pool_size=POOL_SIZE, pool_pre_ping=True)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

class VideoData(Base):
    __tablename__ = MYSQL_TABLENAME

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    publishing_datetime = Column(DateTime)
    thumbnail_urls = Column(String)
    video_url = Column(String)


async def write_query(video_data_list: List[VideoDataModel]):
    async with Session() as session:
        async with session.begin():
            video_data_row_list = []
            for video_data in video_data_list:
                video_data_row = VideoData(
                    title=video_data.title, 
                    description=video_data.description, 
                    publishing_datetime=video_data.publishing_datetime,
                    thumbnail_urls=video_data.thumbnail_urls,
                    video_url=video_data.video_url
                )

                video_data_row_list.append(video_data_row)
            session.add_all(video_data_row_list)

            await session.commit()


async def get_query():
    async with Session() as session:
        output = []
        async with session.begin():
            result = await session.execute(select(VideoData))
            output = result.scalars().all()

            await session.commit()
        return output


async def search_query(search_string: str):
    search_string = "%" + search_string.replace(" ", "%") + "%"

    async with Session() as session:
        output = []
        async with session.begin():
            result = await session.execute(
                        select(VideoData).filter(
                            or_(
                                VideoData.title.like(search_string), 
                                VideoData.description.like(search_string)
                            )
                        )
                    )
            try:
                output = result.scalars.all()
            except Exception as e:
                output = []

            await session.commit()
        return output