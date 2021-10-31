from typing import Any, List

import requests
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

class Event(BaseModel):
    type: str
    payload: Any

events: List[Event] = []


@app.post("/events/")
def create_event(event: Event):
    
    events.append(event)
    
    logger.debug(f"Received event: {event.type}")
    requests.post("http://localhost:4000/events/", data=event)
    requests.post("http://localhost:4001/events/", data=event)
    requests.post("http://localhost:4002/events/", data=event)

    logger.debug("Passed events")


if __name__ == "__main__":
    uvicorn.run(app, debug=True, host="0.0.0.0", port=4003)
