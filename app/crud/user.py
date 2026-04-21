from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.user import User as UserModel
from app.schema.user import User

async def get_user(db: Session, UserID: int):
    return db.query(UserModel).filter(UserModel.UserID == UserID).first()

async def create_user(db: Session, user: User):
    new_user = UserModel(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def get_user_by_username(db: Session, Username: str):
    return db.query(UserModel).filter(UserModel.Username == Username).first()
