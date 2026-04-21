from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.owns import Owns as OwnsModel
from app.schema.owns import Owns

async def get_owns(db: Session, DLNum: int, VIN: str):
    return db.query(OwnsModel).filter(OwnsModel.DLNum == DLNum, OwnsModel.VIN == VIN).first()

async def create_owns(db: Session, owns: Owns):
    new_owns = OwnsModel(**owns.dict())
    
    db.add(new_owns)
    db.commit()
    db.refresh(new_owns)
    return new_owns

async def delete_owns(db: Session, DLNum: int, VIN: str):
    owns = db.query(OwnsModel).filter(OwnsModel.DLNum == DLNum, OwnsModel.VIN == VIN).first()
    if not owns:
        raise HTTPException(status_code=404, detail="Owns relationship not found")
    
    db.delete(owns)
    db.commit()
    return {"detail": "Owns relationship deleted successfully"}

async def update_owns(db: Session, DLNum: int, VIN: str, owns: Owns):
    existing_owns = db.query(OwnsModel).filter(OwnsModel.DLNum == DLNum, OwnsModel.VIN == VIN).first()
    if not existing_owns:
        raise HTTPException(status_code=404, detail="Owns relationship not found")

    for key, value in owns.dict().items():
        setattr(existing_owns, key, value)

    db.commit()
    db.refresh(existing_owns)
    return existing_owns