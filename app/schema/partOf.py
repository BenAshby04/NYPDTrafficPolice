from pydantic import BaseModel

class PartOf(BaseModel):
    DetatchID: int
    DistrictID: int