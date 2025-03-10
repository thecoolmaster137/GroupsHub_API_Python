from pydantic import BaseModel

class AddApplication(BaseModel):
    name: str
