from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class NoticeAction(Base):
    __tablename__ = "NoticeAction"
    NID: Mapped[int] = mapped_column("NID", Integer, ForeignKey("Notice.NID"), primary_key=True, nullable=False)
    ActCode: Mapped[str] = mapped_column("ActCode", String(50), ForeignKey("ActionCode.ActCode"), nullable=False)