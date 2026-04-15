from pydantic import BaseModel

class Lives(BaseModel):
    DLNum: str
    Number: int
    ZipCode: str