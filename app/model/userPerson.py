from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class UserPerson(Base):
    __tablename__ = "UserPerson"
    UserID: Mapped[int] = mapped_column("UserID", Integer,ForeignKey("User.UserID"), primary_key=True, nullable=False)
    DLNum: Mapped[str] = mapped_column("DLNum", String(50),ForeignKey("Person.DLNum"),primary_key=True, nullable=False)