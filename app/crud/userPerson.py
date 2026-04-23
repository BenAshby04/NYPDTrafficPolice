from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.model.userPerson import UserPerson as UserPersonModel
from app.schema.userPerson import UserPerson

async def get_link_by_user(db: Session, UserID: int):
    return db.query(UserPersonModel).filter(UserPersonModel.UserID == UserID).first()

async def get_link_by_dlnum(db:Session, DLNum:str):
    return db.query(UserPersonModel).filter(UserPersonModel.DLNum == DLNum).first()

async def create_link(db:Session, link:UserPerson):
    existing_user_link = db.query(UserPersonModel).filter(UserPersonModel.UserID == link.UserID).first()
    if existing_user_link:
        raise HTTPException(status_code=400, detail="User is already linked to a Person")
    
    existing_dl_link = db.query(UserPersonModel).filter(UserPersonModel.DLNum == link.DLNum).first()
    if existing_dl_link:
        raise HTTPException(status_code=400, detail="Person is already linked to a User")
    
    new_link = UserPersonModel(**link.dict())
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link

async def delete_link(db:Session, UserID: int):
    existing = db.query(UserPersonModel).filter(UserPersonModel.UserID == UserID).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Link not found")
    
    db.delete(existing)
    db.commit()
    return {"message": "Link Deleted Successfully!"}