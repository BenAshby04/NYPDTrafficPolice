from pydantic import BaseModel

class Vehicle(BaseModel):
    VIN: str
    LPlate: str
    StatePlate: str
    Year: int
    Make: str