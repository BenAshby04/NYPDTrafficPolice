from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.district import District
from app.crud.district import get_district, create_district

router = APIRouter(prefix="/district", tags=["district"])

@router.get("/{DistrictID}", response_model=District)
async def get_district_by_id(DistrictID: int, db: Session = Depends(get_db)):
    district = await get_district(db, DistrictID)
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@router.post("/", response_model=District)
async def create_new_district(district: District, db: Session = Depends(get_db)):
    return await create_district(db, district)