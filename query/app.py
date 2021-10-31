from typing import Any, Dict, List

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
    id: str
    comment: str


class Post(BaseModel):
    id: str
    title: str
    comments: List[Comment]


class Event(BaseModel):
    type: str
    payload: Any


Posts = Dict[str, Post]

posts: Posts = {}


@app.get("/posts/", response_model=Posts)
def get_posts():
    logger.debug(f"Found  {len(posts)} posts")
    return posts


@app.post("/events/")
def event_handler(event: Event):

    if event.type == "PostCreated":
        id = event.payload["id"]
        title = event.payload["title"]
        posts[id] = Post(id=id, title=title, comments=[])

    if event.type == "CommentCreated":
        post_id = event.payload["comment"]["post_id"]
        comment = event.payload["comment"]["comment"]
        id = event.payload["id"]
        posts[post_id].comments.append(Comment(id=id, comment=comment))
