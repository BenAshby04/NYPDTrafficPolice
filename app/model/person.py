from sqlalchemy import String, Integer, ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import date

class Person(Base):
    __tablename__ = "Person"
    DLNum: Mapped[str] = mapped_column("DLNum", String(50), primary_key=True, nullable=False)
    FName: Mapped[str] = mapped_column("FName", String(50), nullable=False)
    LName: Mapped[str] = mapped_column("LName", String(50), nullable=False)
    DOB: Mapped[date] = mapped_column("DOB", Date, nullable=False)
    Height: Mapped[float] = mapped_column("Height", Numeric(4,1), nullable=False)
    Weight: Mapped[float] = mapped_column("WEIGHT", Numeric(4,1), nullable=False)
    EyeColor: Mapped[str] = mapped_column("EyeColor", String(50), nullable=False)
    DLState: Mapped[str] = mapped_column("DLState", String(25), nullable=False)