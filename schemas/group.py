from pydantic import BaseModel
from typing import Optional

class Group(BaseModel):
    group_id: int
    group_name: str
    group_link: str
    group_image: str
    cat_name: Optional[str] = None
    cat_id: Optional[int] = None
    country: str
    language: str
    group_desc: Optional[str] = None
    group_rules: Optional[str] = None
    tags: Optional[str] = None
    message: Optional[str] = None
