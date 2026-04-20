from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.address import Address as AddressModel
from app.schema.address import Address

async def get_address(db: Session, AddressID: int):
    return db.query(AddressModel).filter(AddressModel.AddressID == AddressID).first()

async def create_address(db: Session, address: Address):
    new_address = AddressModel(**address.dict())
    
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address