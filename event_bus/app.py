from typing import Any, Dict, List

import requests
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
def create_event(event: Event):

    events.append(event)

    logger.debug(f"Received event: {event.type}")
    requests.post("http://localhost:4000/events/", json=event.dict())
    requests.post("http://localhost:4001/events/", json=event.dict())
    requests.post("http://localhost:4002/events/", json=event.dict())

    logger.debug("Passed events")
