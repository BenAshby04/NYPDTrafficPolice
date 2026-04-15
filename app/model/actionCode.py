from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ActionCode(Base):
    __tablename__ = "ActionCode"
    ActCode: Mapped[str] = mapped_column("ActCode", String(50), primary_key=True,nullable=False)
    Description: Mapped[str] = mapped_column("Description", String(255), nullable=False)