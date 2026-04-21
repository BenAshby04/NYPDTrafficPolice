from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.officer import Officer
from app.crud.officer import get_officer, create_officer, update_officer, delete_officer

router = APIRouter(prefix="/officer", tags=["officer"])
@router.get("/{OfficerID}", response_model=Officer)
async def get_officer_by_id(OfficerID: int, db: Session = Depends(get_db)):
    officer = await get_officer(db, OfficerID)
    if officer is None:
        raise HTTPException(status_code=404, detail="Officer not found")
    return officer

@router.post("/", response_model=Officer)
async def create_new_officer(officer: Officer, db: Session = Depends(get_db)):
    return await create_officer(db, officer)

@router.put("/{OfficerID}", response_model=Officer)
async def update_officer_by_id(OfficerID: int, officer: Officer, db: Session = Depends(get_db)):
    return await update_officer(db, OfficerID, officer)

@router.delete("/{OfficerID}")
async def delete_officer_by_id(OfficerID: int, db: Session = Depends(get_db)):
    return await delete_officer(db, OfficerID)