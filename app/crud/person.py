from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.person import Person as PersonModel
from app.schema.person import Person

async def get_person(db: Session, DLNum: str):
    return db.query(PersonModel).filter(PersonModel.DLNum == DLNum).first()

async def create_person(db: Session, person: Person):
    new_person = PersonModel(**person.dict())
    
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

async def update_person(db: Session, DLNum: str, person: Person):
    existing_person = db.query(PersonModel).filter(PersonModel.DLNum == DLNum).first()
    if not existing_person:
        raise HTTPException(status_code=404, detail="Person not found")

    for key, value in person.dict().items():
        setattr(existing_person, key, value)

    db.commit()
    db.refresh(existing_person)
    return existing_person

async def delete_person(db: Session, DLNum: str):
    existing_person = db.query(PersonModel).filter(PersonModel.DLNum == DLNum).first()
    if not existing_person:
        raise HTTPException(status_code=404, detail="Person not found")

    db.delete(existing_person)
    db.commit()
    return {"message": "Person deleted successfully!"}