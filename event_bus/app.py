from typing import Dict, List

import requests_async as requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    type: str
    payload: Dict


events: List[Event] = []


@app.post("/events/")
async def create_event(event: Event):

    events.append(event)

    logger.debug(f"Received event: {event.type}")
    await requests.post("http://posts-srv:4000/events/", json=event.dict())
    await requests.post("http://comments-srv:4001/events/", json=event.dict())
    await requests.post("http://query-srv:4002/events/", json=event.dict())
    await requests.post("http://moderator-srv:4004/events/", json=event.dict())

    logger.debug(f"Passed event: {event.type}")
