from pydantic import BaseModel
from datetime import date

class Person(BaseModel):
    DLNum: str
    FName: str
    LName: str
    DOB: date
    Height: float
    Weight: float
    EyeColour: str
    DLState: str