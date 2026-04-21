from pydantic import BaseModel

class Registered(BaseModel):
    Number: int
    ZipCode: str
    VIN: str