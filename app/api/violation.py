from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.schema.violation import Violation
from app.crud.violation import get_violations_by_DLNumber, add_violation, update_violation, delete_violation

router = APIRouter(prefix="/violation", tags=["violation"])

@router.get("/dl/{DLNumber}", response_model=dict)
async def get_violations_by_dl_number(DLNumber: str, db: Session = Depends(get_db)):
    return await get_violations_by_DLNumber(db, DLNumber)

@router.get("/stats")
async def get_violation_stats(db:Session = Depends(get_db)):
    total = db.execute(text("SELECT COUNT(*) as count FROM Notice")).mappings().first()
    byType = db.execute(text("SELECT VioCode, COUNT(*) as count FROM NoticeVio GROUP BY VioCode ORDER BY count DESC")).mappings().all()
    return{
        "total_violations": total["count"],
        "by_violation_type": [dict(r) for r in byType]
    }

@router.post("/", response_model=dict)
async def create_new_violation(violation: Violation, db: Session = Depends(get_db)):
    return await add_violation(db, violation.violation_date,violation.violation_time,violation.location,violation.DLNum,violation.PID,violation.VIN,violation.vioCode,violation.notes,violation.actCode)

@router.put("/{ViolationID}", response_model=dict)
async def update_violation_by_id(ViolationID: int, violation: Violation, db: Session = Depends(get_db)):
    return await update_violation(db, ViolationID, violation.violation_date,violation.violation_time,violation.location,violation.DLNum,violation.PID,violation.VIN,violation.vioCode,violation.notes,violation.actCode)

@router.delete("/{ViolationID}")
async def delete_violation_by_id(ViolationID: int, db: Session = Depends(get_db)):
    return await delete_violation(db, ViolationID)