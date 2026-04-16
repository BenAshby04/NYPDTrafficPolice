from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.officer import Officer as OfficerModel
from app.schema.officer import Officer

async def get_officer(db: Session, PID: int):
    return db.query(OfficerModel).filter(OfficerModel.PID == PID).first()

async def create_officer(db: Session, officer: Officer):
    new_officer = OfficerModel(**officer.dict())
    
    db.add(new_officer)
    db.commit()
    db.refresh(new_officer)
    return new_officer