from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.district import District as DistrictModel
from app.schema.district import District

async def get_district(db: Session, DistrictID: int):
    return db.query(DistrictModel).filter(DistrictModel.DistrictID == DistrictID).first()

async def create_district(db: Session, district: District):
    new_district = DistrictModel(**district.dict())
    
    db.add(new_district)
    db.commit()
    db.refresh(new_district)
    return new_district