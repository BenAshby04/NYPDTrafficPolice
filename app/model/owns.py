from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Owns(Base):
    __tablename__ = "Owns"
    DLNum: Mapped[str] = mapped_column("DLNum", String(50), ForeignKey("Person.DLNum"), primary_key=True, nullable=False)
    VIN: Mapped[str] = mapped_column("VIN", String(50), ForeignKey("Vehicle.VIN"), primary_key=True, nullable=False)