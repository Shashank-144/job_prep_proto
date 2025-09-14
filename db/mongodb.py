import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from pydantic import BaseModel
import certifi
from typing import Optional
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"   # local fallback for development
)

client = AsyncIOMotorClient(MONGO_URI,tls=True,tlsCAFile=certifi.where())    # motor client
db = client["job_search_buddy"]           # explicit DB name
feedback_collection = db["feedbacks"]     # collection


class Feedback(BaseModel):
    
    job_role: str
    feedback_text: str
    rating: Optional[int] = None