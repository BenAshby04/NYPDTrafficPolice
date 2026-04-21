from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.violationCode import ViolationCode as ViolationCodeModel
from app.schema.violationCode import ViolationCode

async def get_violationCode(db: Session, VioCode: int):
    return db.query(ViolationCodeModel).filter(ViolationCodeModel.VioCode == VioCode).first()

async def create_violationCode(db: Session, violationCode: ViolationCode):
    new_violationCode = ViolationCodeModel(**violationCode.dict())
    
    db.add(new_violationCode)
    db.commit()
    db.refresh(new_violationCode)
    return new_violationCode

async def update_violationCode(db: Session, VioCode: int, violationCode: ViolationCode):
    existing_violationCode = db.query(ViolationCodeModel).filter(ViolationCodeModel.VioCode == VioCode).first()
    
    if not existing_violationCode:
        raise HTTPException(status_code=404, detail="Violation code not found")
    
    for key, value in violationCode.dict().items():
        setattr(existing_violationCode, key, value)
    
    db.commit()
    db.refresh(existing_violationCode)
    return existing_violationCode

async def delete_violationCode(db: Session, VioCode: int):
    existing_violationCode = db.query(ViolationCodeModel).filter(ViolationCodeModel.VioCode == VioCode).first()
    
    if not existing_violationCode:
        raise HTTPException(status_code=404, detail="Violation code not found")
    
    db.delete(existing_violationCode)
    db.commit()
    return {"message": "Violation code deleted successfully!"}

async def get_all_violationCodes(db: Session):
    return db.query(ViolationCodeModel).all()