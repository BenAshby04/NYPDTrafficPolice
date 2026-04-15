from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class PartOf(Base):
    __tablename__ = "PartOf"
    DetatchID: Mapped[int] = mapped_column("DetatchID", Integer, ForeignKey("Detatchment.DetatchID"), primary_key=True, nullable=False)
    DistrictID: Mapped[int] = mapped_column("DistrictID", Integer, ForeignKey("District.DistrictID"), nullable=False)