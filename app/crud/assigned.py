from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.assigned import Assigned as AssignedModel
from app.schema.assigned import Assigned

async def get_assigned(db: Session, DetatchID: int):
    return db.query(AssignedModel).filter(AssignedModel.DetatchID == DetatchID).first()

async def create_assigned(db: Session, assigned: Assigned):
    new_assigned = AssignedModel(**assigned.dict())
    
    db.add(new_assigned)
    db.commit()
    db.refresh(new_assigned)
    return new_assigned

async def update_assigned(db: Session, DetatchID: int, assigned: Assigned):
    existing_assigned = db.query(AssignedModel).filter(AssignedModel.DetatchID == DetatchID).first()
    if not existing_assigned:
        raise HTTPException(status_code=404, detail="Assigned not found")

    for key, value in assigned.dict().items():
        setattr(existing_assigned, key, value)
    db.commit()
    db.refresh(existing_assigned)
    return existing_assigned

