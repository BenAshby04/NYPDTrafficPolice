from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.detatchment import Detatchment
from app.crud.detatchment import get_detatchment, create_detatchment

router = APIRouter(prefix="/detatchment", tags=["detatchment"])

@router.get("/{DetatchmentID}", response_model=Detatchment)
async def get_detatchment_by_id(DetatchmentID: int, db: Session = Depends(get_db)):
    detatchment = await get_detatchment(db, DetatchmentID)
    if detatchment is None:
        raise HTTPException(status_code=404, detail="Detatchment not found")
    return detatchment

@router.post("/", response_model=Detatchment)
async def create_new_detatchment(detatchment: Detatchment, db: Session = Depends(get_db)):
    return await create_detatchment(db, detatchment)