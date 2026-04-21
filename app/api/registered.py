from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.registered import Registered
from app.crud.registered import get_registered, create_registered, update_registered, delete_registered

router = APIRouter(prefix="/registered", tags=["registered"])
@router.get("/{RegisteredID}", response_model=Registered)
async def get_registered_by_id(RegisteredID: int, db: Session = Depends(get_db)):
    registered = await get_registered(db, RegisteredID)
    if registered is None:
        raise HTTPException(status_code=404, detail="Registered not found")
    return registered

@router.post("/", response_model=Registered)
async def create_new_registered(registered: Registered, db: Session = Depends(get_db)):
    return await create_registered(db, registered)

@router.put("/{RegisteredID}", response_model=Registered)
async def update_registered_by_id(RegisteredID: int, registered: Registered, db: Session = Depends(get_db)):
    return await update_registered(db, RegisteredID, registered)

@router.delete("/{RegisteredID}")
async def delete_registered_by_id(RegisteredID: int, db: Session = Depends(get_db)):
    return await delete_registered(db, RegisteredID)