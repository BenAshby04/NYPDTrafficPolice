from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.registered import Registered as RegisteredModel
from app.schema.registered import Registered

async def get_registered(db: Session, Number: int, ZipCode: str, VIN: str):
    return db.query(RegisteredModel).filter(RegisteredModel.Number == Number, RegisteredModel.ZipCode == ZipCode, RegisteredModel.VIN == VIN).first()

async def create_registered(db: Session, registered: Registered):
    new_registered = RegisteredModel(**registered.dict())
    
    db.add(new_registered)
    db.commit()
    db.refresh(new_registered)
    return new_registered

async def delete_registered(db: Session, Number: int, ZipCode: str, VIN: str):
    registered = db.query(RegisteredModel).filter(RegisteredModel.Number == Number, RegisteredModel.ZipCode == ZipCode, RegisteredModel.VIN == VIN).first()
    if not registered:
        raise HTTPException(status_code=404, detail="Registered not found")
    
    db.delete(registered)
    db.commit()
    return {"detail": "Registered deleted successfully"}

async def update_registered(db: Session, Number: int, ZipCode: str, VIN: str, registered: Registered):
    existing_registered = db.query(RegisteredModel).filter(RegisteredModel.Number == Number, RegisteredModel.ZipCode == ZipCode, RegisteredModel.VIN == VIN).first()
    if not existing_registered:
        raise HTTPException(status_code=404, detail="Registered not found")

    for key, value in registered.dict().items():
        setattr(existing_registered, key, value)

    db.commit()
    db.refresh(existing_registered)
    return existing_registered