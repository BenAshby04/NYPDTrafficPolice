from sqlalchemy import String, Integer, ForeignKey, Date, Time
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import date, time

class Notice(Base):
    __tablename__ = "Notice"
    NID: Mapped[int] = mapped_column("NID", Integer, primary_key=True, nullable=False, autoincrement=True)
    Date: Mapped[date] = mapped_column("Date", Date, nullable=False)
    Time: Mapped[time] = mapped_column("Time", Time, nullable=False)
    Location: Mapped[str] = mapped_column("Location", String(50), nullable=False)