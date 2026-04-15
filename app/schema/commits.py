from pydantic import BaseModel

class Commits(BaseModel):
    DLNum: str
    NID: int