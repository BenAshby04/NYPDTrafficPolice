from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.partOf import PartOf as PartOfModel
from app.schema.partOf import PartOf

async def get_partOf(db: Session, DetatchID: int):
    return db.query(PartOfModel).filter(PartOfModel.DetatchID == DetatchID).first()

async def create_partOf(db: Session, partOf: PartOf):
    new_partOf = PartOfModel(**partOf.dict())
    
    db.add(new_partOf)
    db.commit()
    db.refresh(new_partOf)
    return new_partOf