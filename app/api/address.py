from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.address import Address
from app.crud.address import get_address, create_address

router = APIRouter(prefix="/address", tags=["address"])

@router.get("/{Number}/{ZipCode}", response_model=Address)
async def get_address_by_id(Number: int, ZipCode: str, db: Session = Depends(get_db)):
    address = await get_address(db, Number, ZipCode)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.post("/", response_model=Address)
async def create_new_address(address: Address, db: Session = Depends(get_db)):
    return await create_address(db, address)