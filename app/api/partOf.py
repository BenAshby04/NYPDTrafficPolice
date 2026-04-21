from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.partOf import PartOf
from app.crud.partOf import get_partOf, create_partOf

router = APIRouter(prefix="/partOf", tags=["partOf"])
@router.get("/{PartOfID}", response_model=PartOf)
async def get_partOf_by_id(PartOfID: int, db: Session = Depends(get_db)):
    partOf = await get_partOf(db, PartOfID)
    if partOf is None:
        raise HTTPException(status_code=404, detail="PartOf not found")
    return partOf

@router.post("/", response_model=PartOf)
async def create_new_partOf(partOf: PartOf, db: Session = Depends(get_db)):
    return await create_partOf(db, partOf)