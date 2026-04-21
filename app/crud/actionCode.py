from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.actionCode import ActionCode as ActionCodeModel
from app.schema.actionCode import ActionCode

async def get_actionCode(db: Session, ActionCodeID: int):
    return db.query(ActionCodeModel).filter(ActionCodeModel.ActCode == ActionCodeID).first()

async def create_actionCode(db: Session, actionCode: ActionCode):
    new_actionCode = ActionCodeModel(**actionCode.dict())
    
    db.add(new_actionCode)
    db.commit()
    db.refresh(new_actionCode)
    return new_actionCode

async def update_actionCode(db: Session, ActionCodeID: int, actionCode: ActionCode):
    existing_actionCode = db.query(ActionCodeModel).filter(ActionCodeModel.ActCode == ActionCodeID).first()
    
    if not existing_actionCode:
        raise HTTPException(status_code=404, detail="ActionCode not found")
    
    for key, value in actionCode.dict().items():
        setattr(existing_actionCode, key, value)
    
    db.commit()
    db.refresh(existing_actionCode)
    return existing_actionCode

async def delete_actionCode(db: Session, ActionCodeID: int):
    existing_actionCode = db.query(ActionCodeModel).filter(ActionCodeModel.ActCode == ActionCodeID).first()
    
    if not existing_actionCode:
        raise HTTPException(status_code=404, detail="ActionCode not found")
    
    db.delete(existing_actionCode)
    db.commit()
    return {"message": "ActionCode deleted successfully!"}

async def get_all_actionCodes(db: Session):
    return db.query(ActionCodeModel).all()