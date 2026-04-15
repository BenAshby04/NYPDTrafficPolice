from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class District(Base):
    __tablename__ = "District"
    DistrictID: Mapped[int] = mapped_column("DistrictID", Integer, primary_key=True, nullable=False, autoincrement=True)
    DistrictName: Mapped[str] = mapped_column("DistrictName", String(50), nullable=False)