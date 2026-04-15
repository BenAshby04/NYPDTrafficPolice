from pydantic import BaseModel

class noticeAction(BaseModel):
    NID: int
    ActCode: str