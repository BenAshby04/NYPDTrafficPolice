from pydantic import BaseModel
from datetime import date, time

class Notice(BaseModel):
    NID: int
    Date: date
    Time: time
    Location: str