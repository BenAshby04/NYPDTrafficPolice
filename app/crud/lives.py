from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.lives import Lives as LivesModel
from app.schema.lives import Lives

async def get_lives(db: Session, DLNum: int):
    return db.query(LivesModel).filter(LivesModel.DLNum == DLNum).first()

async def create_lives(db: Session, lives: Lives):
    new_lives = LivesModel(**lives.dict())
    
    db.add(new_lives)
    db.commit()
    db.refresh(new_lives)
    return new_lives

