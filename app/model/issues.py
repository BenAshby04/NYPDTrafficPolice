from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Issues(Base):
    __tablename__ = "Issues"

    NID: Mapped[int] = mapped_column("NID", Integer, ForeignKey("Notice.NID"), primary_key=True, nullable=False)
    PID: Mapped[int] = mapped_column("PID", Integer, ForeignKey("Officer.PID"), primary_key=True, nullable=False)