from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Detatchment(Base):
    __tablename__ = "Detatchment"
    DetatchID: Mapped[int] = mapped_column("DetatchID", Integer, primary_key=True, nullable=False, autoincrement=True)
    DetatchName: Mapped[str] = mapped_column("DetatchName", String(50), nullable=False)