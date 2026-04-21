from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.violationCode import ViolationCode
from app.crud.violationCode import get_violationCode, create_violationCode, update_violationCode, delete_violationCode  

router = APIRouter(prefix="/violation-code", tags=["violation-code"])
@router.get("/{ViolationCodeID}", response_model=ViolationCode)
async def get_violation_code_by_id(ViolationCodeID: int, db: Session = Depends(get_db)):
    violation_code = await get_violationCode(db, ViolationCodeID)
    if violation_code is None:
        raise HTTPException(status_code=404, detail="Violation code not found")
    return violation_code

@router.post("/", response_model=ViolationCode)
async def create_new_violation_code(violation_code: ViolationCode, db: Session = Depends(get_db)):
    return await create_violationCode(db, violation_code)

@router.put("/{ViolationCodeID}", response_model=ViolationCode)
async def update_violation_code_by_id(ViolationCodeID: int, violation_code: ViolationCode, db: Session = Depends(get_db)):
    return await update_violationCode(db, ViolationCodeID, violation_code)

@router.delete("/{ViolationCodeID}")
async def delete_violation_code_by_id(ViolationCodeID: int, db: Session = Depends(get_db)):
    return await delete_violationCode(db, ViolationCodeID)