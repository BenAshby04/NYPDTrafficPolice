from pydantic import BaseModel
from datetime import date, time


class Violation(BaseModel):
    violation_date: date
    violation_time: time
    location: str
    DLNum: str
    PID: int
    VIN: str
    vioCode: str
    notes: str
    actCode: str