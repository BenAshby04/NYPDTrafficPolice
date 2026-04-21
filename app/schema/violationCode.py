from pydantic import BaseModel

class ViolationCode(BaseModel):
    VioCode: str
    Description: str