from pydantic import BaseModel

class User(BaseModel):
    UserID: int
    Username: str
    HashedPassword: str
    UserRole: str