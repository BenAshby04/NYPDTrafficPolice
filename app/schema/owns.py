from pydantic import BaseModel

class Owns(BaseModel):
    DLNum: str
    VIN: str