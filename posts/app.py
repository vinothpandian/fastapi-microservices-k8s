from typing import Any, Dict
from uuid import uuid4

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


class CreatePostRequest(BaseModel):
    title: str


class Event(BaseModel):
    type: str
    payload: Any


posts: Dict[str, str] = {}


@app.post("/posts/create/")
async def create_post(create_post_request: CreatePostRequest):

    id: str = uuid4().hex
    posts[id] = create_post_request.title
    logger.debug(f"Post created with id: {id}")

    await requests.post(
        "http://localhost:4003/events/",
        json={
            "type": "PostCreated",
            "payload": {"id": id, "title": create_post_request.title},
        },
    )

    return id


@app.post("/events/")
def event_handler(event: Event):
    pass
