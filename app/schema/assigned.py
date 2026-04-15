from pydantic import BaseModel

class Assigned(BaseModel):
    PID: int
    DetatchID: int