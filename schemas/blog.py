from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class Blog(BaseModel):
    title: str
    description: str
    image: Optional[HttpUrl] = None
    date: datetime = datetime.utcnow()
