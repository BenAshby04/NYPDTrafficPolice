from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Officer(Base):
    __tablename__ = "Officer"
    PID: Mapped[int] = mapped_column("PID", Integer, primary_key=True, nullable=False, unique=True)
    FName: Mapped[str] = mapped_column("FName", String(50), nullable=False)
    LName: Mapped[str] = mapped_column("LName", String(50), nullable=False)
