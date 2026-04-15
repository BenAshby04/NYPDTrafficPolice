from pydantic import BaseModel

class Officer(BaseModel):
    PID: int
    FName: str
    LName: str