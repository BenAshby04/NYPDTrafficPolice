from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.person import Person
from app.crud.person import get_person, create_person, update_person, delete_person

router = APIRouter(prefix="/person", tags=["person"])

@router.get("/{DLNum}", response_model=Person)
async def get_person_by_id(DLNum: int, db: Session = Depends(get_db)):
    person = await get_person(db, DLNum)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/", response_model=Person)
async def create_new_person(person: Person, db: Session = Depends(get_db)):
    return await create_person(db, person)

@router.put("/{PersonID}", response_model=Person)
async def update_person_by_id(PersonID: int, person: Person, db: Session = Depends(get_db)):
    return await update_person(db, PersonID, person)

@router.delete("/{PersonID}")
async def delete_person_by_id(PersonID: int, db: Session = Depends(get_db)):
    return await delete_person(db, PersonID)