import os
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.future import select

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


async def query():
    async with Session() as session:
        async with session.begin():
            result = await session.execute(select(VideoData).order_by(VideoData.id))
            a1 = result.scalars().first()

            await session.commit()
            
            if a1 is not None:
                print(a1.data)
            else:
                print("a1 is None!")