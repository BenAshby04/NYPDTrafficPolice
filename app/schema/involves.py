from pydantic import BaseModel

class Involves(BaseModel):
    NID: int
    VIN: str