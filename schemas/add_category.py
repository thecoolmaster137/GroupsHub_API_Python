from pydantic import BaseModel

class AddCategory(BaseModel):
    name: str
