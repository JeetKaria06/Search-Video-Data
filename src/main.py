from fastapi import FastAPI
from src.db import query

app = FastAPI()

@app.get("/health")
async def health():
    await query()
    return ["Hi from Fampay Backend Assignment!"]
