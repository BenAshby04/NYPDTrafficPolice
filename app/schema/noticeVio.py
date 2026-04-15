from pydantic import BaseModel

class NoticeVio(BaseModel):
    NID: int
    ItemID: int
    VioCode: str
    Notes: str