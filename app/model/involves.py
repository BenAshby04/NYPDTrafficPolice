from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Involves(Base):
    __tablename__ = "Involves"
    NID: Mapped[int] = mapped_column("NID", Integer, ForeignKey("Notice.NID"), primary_key=True, nullable=False)
    VIN: Mapped[str] = mapped_column("VIN", String(50), ForeignKey("Vehicle.VIN"), primary_key=True, nullable=False)