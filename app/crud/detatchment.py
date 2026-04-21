from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.detatchment import Detatchment as DetatchmentModel
from app.schema.detatchment import Detatchment

async def get_detatchment(db: Session, DetatchID: int):
    return db.query(DetatchmentModel).filter(DetatchmentModel.DetatchID == DetatchID).first()

async def create_detatchment(db: Session, detatchment: Detatchment):
    new_detatchment = DetatchmentModel(**detatchment.dict())
    
    db.add(new_detatchment)
    db.commit()
    db.refresh(new_detatchment)
    return new_detatchment
