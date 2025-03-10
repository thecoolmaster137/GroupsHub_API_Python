from pydantic import BaseModel

class Application(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True 