from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class User(Base):
    __tablename__ = "User"
    UserID: Mapped[int] = mapped_column("UserID", Integer, primary_key= True, nullable=False)
    Username: Mapped[str] = mapped_column("Username", String(50), nullable=False)
    HashedPassword: Mapped[str] = mapped_column("HashedPassword", String(50), nullable=False)
    UserRole: Mapped[str] = mapped_column("UserRole", String(50), nullable=False)