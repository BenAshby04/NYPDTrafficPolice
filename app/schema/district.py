from pydantic import BaseModel

class District(BaseModel):
    DistrictID: int
    DistrictName: str