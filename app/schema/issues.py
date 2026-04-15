from pydantic import BaseModel

class Issues(BaseModel):
    NID: int
    PID: int