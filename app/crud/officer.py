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

async def update_officer(db: Session, PID: int, officer: Officer):
    existing_officer = db.query(OfficerModel).filter(OfficerModel.PID == PID).first()
    if not existing_officer:
        raise HTTPException(status_code=404, detail="Officer not found")

    for key, value in officer.dict().items():
        setattr(existing_officer, key, value)

    db.commit()
    db.refresh(existing_officer)
    return existing_officer 

async def delete_officer(db: Session, PID: int):
    existing_officer = db.query(OfficerModel).filter(OfficerModel.PID == PID).first()
    if not existing_officer:
        raise HTTPException(status_code=404, detail="Officer not found")

    db.delete(existing_officer)
    db.commit()
    return {"message": "Officer deleted successfully!"}