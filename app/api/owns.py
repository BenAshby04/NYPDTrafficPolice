from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.owns import Owns
from app.crud.owns import get_owns, create_owns, update_owns, delete_owns

router = APIRouter(prefix="/owns", tags=["owns"])

@router.get("/{OwnsID}", response_model=Owns)
async def get_owns_by_id(OwnsID: int, db: Session = Depends(get_db)):
    owns = await get_owns(db, OwnsID)
    if owns is None:
        raise HTTPException(status_code=404, detail="Owns not found")
    return owns

@router.post("/", response_model=Owns)
async def create_new_owns(owns: Owns, db: Session = Depends(get_db)):
    return await create_owns(db, owns)

@router.put("/{OwnsID}", response_model=Owns)
async def update_owns_by_id(OwnsID: int, owns: Owns, db: Session = Depends(get_db)):
    return await update_owns(db, OwnsID, owns)

@router.delete("/{OwnsID}")
async def delete_owns_by_id(OwnsID: int, db: Session = Depends(get_db)):
    return await delete_owns(db, OwnsID)