from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.vehicle import Vehicle
from app.crud.vehicle import get_vehicle, create_vehicle, update_vehicle, delete_vehicle

router = APIRouter(prefix="/vehicle", tags=["vehicle"])

@router.get("/{VehicleID}", response_model=Vehicle)
async def get_vehicle_by_id(VehicleID: int, db: Session = Depends(get_db)):
    vehicle = await get_vehicle(db, VehicleID)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.post("/", response_model=Vehicle)
async def create_new_vehicle(vehicle: Vehicle, db: Session = Depends(get_db)):
    return await create_vehicle(db, vehicle)

@router.put("/{VehicleID}", response_model=Vehicle)
async def update_vehicle_by_id(VehicleID: int, vehicle: Vehicle, db: Session = Depends(get_db)):
    return await update_vehicle(db, VehicleID, vehicle)

@router.delete("/{VehicleID}")
async def delete_vehicle_by_id(VehicleID: int, db: Session = Depends(get_db)):
    return await delete_vehicle(db, VehicleID)