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


class CreateCommentRequest(BaseModel):
    post_id: str
    comment: str


class Comment(CreateCommentRequest):
    accepted: bool


class Event(BaseModel):
    type: str
    payload: Any


comments: Dict[str, Comment] = {}


@app.post("/comments/create/")
async def create_comment(create_comment_request: CreateCommentRequest):

    id: str = uuid4().hex
    comment = Comment(
        post_id=create_comment_request.post_id,
        comment=create_comment_request.comment,
        accepted=False,
    )
    comments[id] = comment
    logger.debug(f"Comment created with id: {id}")

    await requests.post(
        "http://event-bus-srv:4003/events/",
        json={
            "type": "CommentCreated",
            "payload": {"id": id, "comment": comment.dict()},
        },
    )

    logger.debug(f"Found {len(comments)}")
    return id


@app.post("/events/")
async def event_handler(event: Event):
    if event.type == "CommentAccepted":
        logger.debug("Updating moderated comment")
        id = event.payload["id"]
        comment = comments[id]
        comment.accepted = True

        await requests.post(
            "http://event-bus-srv:4003/events/",
            json={
                "type": "CommentUpdated",
                "payload": {
                    "id": id,
                    "post_id": comment.post_id,
                    "comment": comment.dict(),
                },
            },
        )

        logger.debug(f"Found {len(comments)}")
        return

    if event.type == "CommentRejected":
        logger.debug("Deleting moderated comment")
        id = event.payload["id"]
        comment = comments[id]

        await requests.post(
            "http://event-bus-srv:4003/events/",
            json={
                "type": "CommentDeleted",
                "payload": {"post_id": comment.post_id, "comment_id": id},
            },
        )
        del comments[id]

        logger.debug(f"Found {len(comments)}")
        return
