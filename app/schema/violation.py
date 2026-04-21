from pydantic import BaseModel

class Violation(BaseModel):
    violation_date: str
    violation_time: str
    location: str
    DLNum: str
    PID: int
    VIN: str
    vioCode: str
    notes: str
    actCode: str