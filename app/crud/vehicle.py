from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.vehicle import Vehicle as VehicleModel
from app.schema.vehicle import Vehicle

async def get_vehicle(db: Session, VIN: str):
    return db.query(VehicleModel).filter(VehicleModel.VIN == VIN).first()

async def create_vehicle(db: Session, vehicle: Vehicle):
    new_vehicle = VehicleModel(**vehicle.dict())
    
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

async def update_vehicle(db: Session, VIN: str, vehicle: Vehicle):
    existing_vehicle = db.query(VehicleModel).filter(VehicleModel.VIN == VIN).first()
    if not existing_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    for key, value in vehicle.dict().items():
        setattr(existing_vehicle, key, value)

    db.commit()
    db.refresh(existing_vehicle)
    return existing_vehicle

async def delete_vehicle(db: Session, VIN: str):
    existing_vehicle = db.query(VehicleModel).filter(VehicleModel.VIN == VIN).first()
    if not existing_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(existing_vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully!"}