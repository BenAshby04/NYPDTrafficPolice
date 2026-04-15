from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Assigned(Base):
    __tablename__ = "Assigned"
    PID : Mapped[int] = mapped_column("PID", Integer, ForeignKey("Officer.PID"), primary_key=True, nullable=False)
    DetatchID : Mapped[int] = mapped_column("DetatchID", Integer, ForeignKey("Detatchment.DetatchID"), primary_key=True, nullable=False)