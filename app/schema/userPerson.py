from pydantic import BaseModel

class UserPerson(BaseModel):
    UserID: int
    DLNum: str