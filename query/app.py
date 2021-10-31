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
    accepted: bool


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
        logger.debug("Adding posts to queries")
        id = event.payload["id"]
        title = event.payload["title"]
        posts[id] = Post(id=id, title=title, comments=[])
        return

    if event.type == "CommentCreated":
        logger.debug("Adding comments to queries")
        comment = event.payload["comment"]
        post_id = comment["post_id"]
        id = event.payload["id"]
        posts[post_id].comments.append(Comment(id=id, **comment))
        return

    if event.type == "CommentUpdated":
        logger.debug("Adding comment update to queries")
        comment_id = event.payload["id"]
        post_id = event.payload["post_id"]
        comment = event.payload["comment"]

        posts[post_id].comments = list(
            filter(lambda comment: comment.id != comment_id, posts[post_id].comments)
        )

        posts[post_id].comments.append(Comment(id=comment_id, **comment))

        logger.debug(posts)
        return

    if event.type == "CommentDeleted":
        logger.debug("Deleting comment from queries")
        post_id = event.payload["post_id"]
        comment_id = event.payload["comment_id"]

        posts[post_id].comments = list(
            filter(lambda comment: comment.id != comment_id, posts[post_id].comments)
        )
        return
