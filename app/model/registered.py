from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Registered(Base):
    __tablename__ = "Registered"
    Number: Mapped[int] = mapped_column("Number", Integer, ForeignKey("Address.Number"), primary_key=True, nullable=False)
    ZipCode: Mapped[str] = mapped_column("ZipCode", String(50), ForeignKey("Address.ZipCode"), primary_key=True, nullable=False)
    VIN: Mapped[str] = mapped_column("VIN", String(50), ForeignKey("Vehicle.VIN"), nullable=False)