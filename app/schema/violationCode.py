from pydantic import BaseModel

class violationCode(BaseModel):
    VioCode: str
    Description: str