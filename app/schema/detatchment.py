from pydantic import BaseModel

class Detatchment(BaseModel):
    DetatchID: int
    DetatchName: str