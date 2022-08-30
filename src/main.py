from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_utils.tasks import repeat_every

# from src.db import query
from src.utils import fetch_and_add_video_data
from src.routers import routes

app = FastAPI()

@app.get("/health")
async def health():
    return ["Hi from Fampay Backend Assignment!"]


@app.on_event("startup")
@repeat_every(seconds=10, raise_exceptions=True)
async def add_video_data() -> None:
    await fetch_and_add_video_data()


app.include_router(routes.router)

add_pagination(app)
