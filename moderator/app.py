from time import sleep
from typing import Any

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


class Comment(BaseModel):
    post_id: str
    comment: str
    accepted: bool


class Event(BaseModel):
    type: str
    payload: Any


@app.post("/events/")
async def event_handler(event: Event):

    if event.type != "CommentCreated":
        return

    comment_text = event.payload["comment"]["comment"]
    comment_id = event.payload["id"]

    if "sux" in comment_text:

        logger.debug(f"Rejected comment: {comment_id}")
        await requests.post(
            "http://event-bus-srv:4003/events/",
            json={
                "type": "CommentRejected",
                "payload": {"id": comment_id},
            },
        )

        return

    logger.debug(f"Accepted comment: {comment_id}")

    await requests.post(
        "http://event-bus-srv:4003/events/",
        json={
            "type": "CommentAccepted",
            "payload": {"id": comment_id},
        },
    )
