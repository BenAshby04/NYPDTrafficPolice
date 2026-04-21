from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.user import User as UserModel
from app.schema.user import User
from app.core.security import getPasswordHash

async def get_user(db: Session, UserID: int):
    return db.query(UserModel).filter(UserModel.UserID == UserID).first()

async def create_user(db: Session, user_in: User):
    new_user = UserModel(Username=user_in.Username, HashedPassword=getPasswordHash(user_in.HashedPassword), UserRole=user_in.UserRole)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def get_user_by_username(db: Session, Username: str):
    return db.query(UserModel).filter(UserModel.Username == Username).first()
