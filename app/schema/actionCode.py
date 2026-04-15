from pydantic import BaseModel

class actionCode(BaseModel):
    ActCode: str
    Description: str