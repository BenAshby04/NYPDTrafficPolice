from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Commits(Base):
    __tablename__ = "Commits"
    DLNum: Mapped[str] = mapped_column("DLNum", String(50), ForeignKey("Person.DLNum"), primary_key=True, nullable=False)
    NID: Mapped[int] = mapped_column("NID", Integer, ForeignKey("Notice.NID"), primary_key=True, nullable=False)
