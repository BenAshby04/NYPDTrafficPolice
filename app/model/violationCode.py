from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ViolationCode(Base):
    __tablename__ = "ViolationCode"
    VioCode: Mapped[str] = mapped_column("VioCode", String(50), primary_key=True, nullable=False)
    Description: Mapped[str] = mapped_column("Description", String(255), nullable=False)