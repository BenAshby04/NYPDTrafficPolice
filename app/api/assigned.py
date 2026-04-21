from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.assigned import Assigned
from app.crud.assigned import get_assigned, create_assigned, update_assigned

router = APIRouter(prefix="/assigned", tags=["assigned"])
@router.get("/{AssignedID}", response_model=Assigned)
async def get_assigned_by_id(AssignedID: int, db: Session = Depends(get_db)):
    assigned = await get_assigned(db, AssignedID)
    if assigned is None:
        raise HTTPException(status_code=404, detail="Assigned not found")
    return assigned

@router.post("/", response_model=Assigned)
async def create_new_assigned(assigned: Assigned, db: Session = Depends(get_db)):
    return await create_assigned(db, assigned)

@router.put("/{AssignedID}", response_model=Assigned)
async def update_assigned_by_id(AssignedID: int, assigned: Assigned, db: Session = Depends(get_db)):
    return await update_assigned(db, AssignedID, assigned)