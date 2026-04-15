from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Vehicle(Base):
    __tablename__ = "Vehicle"
    VIN: Mapped[str] = mapped_column("VIN", String(50), primary_key=True, nullable=False)
    LPlate: Mapped[str] = mapped_column("LPlate", String(50), nullable=False)
    StatePlate: Mapped[str] = mapped_column("StatePlate", String(50), nullable=False)
    Year: Mapped[int] = mapped_column("Year", Integer, nullable=False)
    Make: Mapped[str] = mapped_column("Make", String(50), nullable=False)