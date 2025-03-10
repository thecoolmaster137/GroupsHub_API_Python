from pydantic import BaseModel
from typing import Optional

class AddGroup(BaseModel):
    group_link: str
    country: str
    language: str
    group_desc: Optional[str] = None
    group_rules: Optional[str] = None
    tags: Optional[str] = None
