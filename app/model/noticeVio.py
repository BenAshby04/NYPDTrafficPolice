from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class NoticeVio(Base):
    __tablename__ = "NoticeVio"
    NID: Mapped[int] = mapped_column("NID", Integer, ForeignKey("Notice.NID"), primary_key=True, nullable=False)
    ItemID: Mapped[int] = mapped_column("ItemID", Integer, primary_key=True, nullable=False)
    VioCode: Mapped[str] = mapped_column("VioCode", String(50), ForeignKey("ViolationCode.VioCode"), nullable=False)
    Notes: Mapped[str] = mapped_column("Notes", String(100), nullable=False)