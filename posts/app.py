from typing import Dict
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

class CreatePostRequest(BaseModel):
    title: str

posts: Dict[str, str] = {}


@app.post("/posts/create/")
def create_post(create_post_request: CreatePostRequest):

    id: str = uuid4().hex
    posts[id] = create_post_request.title
    logger.debug(f"Post created with id: {id}")
    return id


if __name__ == "__main__":
    uvicorn.run(app, debug=True, host="0.0.0.0", port=4000)
