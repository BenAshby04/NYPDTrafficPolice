from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.violationCode import ViolationCode as ViolationCodeModel
from app.schema.violationCode import ViolationCode

async def get_violation_code(db: Session, vio_code: str):
    return db.query(ViolationCodeModel).filter(ViolationCodeModel.VioCode == vio_code).first()

async def get_violations_by_DLNumber(db: Session, DLNum: str):
    result = db.execute(text("CALL NYPD.GetCiviData(:DLNum)"), {"DLNum": DLNum})

    violations = result.mappings().all()
    result.close()

    if not violations:
        raise HTTPException(status_code=404, detail="No violations found for the provided DLNumber")
    
    return {"Violations": [dict(row) for row in violations]}