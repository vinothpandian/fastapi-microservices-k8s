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

class Comment(BaseModel):
    post_id: str
    comment: str
    

comments: Dict[str, Comment] = {}


@app.post("/comments/create/")
def create_comment(create_comment_request: Comment):

    id: str = uuid4().hex
    comment = Comment(post_id=create_comment_request.post_id, comment=create_comment_request.comment)
    comments[id] = comment
    logger.debug(f"Comment created with id: {id}")
    return id


if __name__ == "__main__":
    uvicorn.run(app, debug=True, host="0.0.0.0", port=4001)
