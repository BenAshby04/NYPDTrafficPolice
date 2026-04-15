from pydantic import BaseModel

class Person(BaseModel):
    DLNum: str
    FName: str
    LName: str
    DOB: str
    Height: float
    Weight: float
    EyeColor: str
    DLState: str