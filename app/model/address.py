from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Address(Base):
    __tablename__ = "Address"
    Number: Mapped[int] = mapped_column("Number", Integer, primary_key= True, nullable=False)
    ZipCode: Mapped[str] = mapped_column("ZipCode", String(50),primary_key=True, nullable=False)
    Street: Mapped[str] = mapped_column("Street", String(50), nullable=False)
    State: Mapped[str] = mapped_column("State", String(50), nullable=False)