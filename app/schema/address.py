from pydantic import BaseModel

class Address(BaseModel):
    Number: int
    ZipCode: str
    Street: str
    State: str