from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Lives(Base):
    __tablename__ = "Lives"
    DLNum: Mapped[str] = mapped_column("DLNum", String(50), ForeignKey("Person.DLNum"), primary_key=True, nullable=False)
    Number: Mapped[int] = mapped_column("Number", Integer, ForeignKey("Address.Number"), primary_key=True, nullable=False)
    ZipCode: Mapped[str] = mapped_column("ZipCode", String(50), ForeignKey("Address.ZipCode"), primary_key=True, nullable=False)