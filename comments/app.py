
from typing import List
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

app = FastAPI()

class CreateCommentRequest(BaseModel):
    post_id: str
    comment: str
    

class Comment(CreateCommentRequest):
    id: str

comments: List[Comment] = []


@app.post("/comments/create")
def create_comment(create_comment_request: CreateCommentRequest):

    id: str = uuid4().hex
    comment = Comment(id=id, post_id=create_comment_request.post_id, comment=create_comment_request.comment)
    comments.append(comment)
    logger.debug(f"Comment created with id: {id}")
    return comment


if __name__ == "__main__":
    uvicorn.run(app, debug=True, host="0.0.0.0", port=4001)
