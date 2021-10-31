from typing import List

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

class Comment(BaseModel):
    id: str
    comment: str

class Post(BaseModel):
    id: str
    title: str
    comments: List[Comment]
    

posts: List[Post] = []


@app.get("/posts/")
def get_posts():
    logger.debug(f"Found  {len(posts)} posts")
    return posts


if __name__ == "__main__":
    uvicorn.run(app, debug=True, host="0.0.0.0", port=4002)
