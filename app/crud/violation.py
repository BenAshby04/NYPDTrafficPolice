from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from app.model.violationCode import ViolationCode as ViolationCodeModel
from app.schema.violationCode import ViolationCode
from datetime import date, time


async def get_violations_by_DLNumber(db: Session, DLNum: str):
    result = db.execute(text("CALL NYPD.GetCiviData(:DLNum)"), {"DLNum": DLNum})

    violations = result.mappings().all()
    result.close()

    if not violations:
        raise HTTPException(status_code=404, detail="No violations found for the provided DLNumber")
    
    return {"Violations": [dict(row) for row in violations]}


async def update_violation(db: Session, NID: int, violation_date: date, violation_time: time, location: str, DLNum: str, PID: int, VIN: str, vioCode: str, notes: str, actCode: str):

    person_exists = db.execute(text("SELECT 1 FROM Person WHERE DLNum = :dl_num LIMIT 1"), {"dl_num": DLNum}).first()
    if not person_exists:
        raise HTTPException(status_code=404, detail="Person with DLNum not found")

    officer_exists = db.execute(text("SELECT 1 FROM Officer WHERE PID = :pid LIMIT 1"), {"pid": PID}).first()
    if not officer_exists:
        raise HTTPException(status_code=404, detail="Officer with PID not found")

    vehicle_exists = db.execute(text("SELECT 1 FROM Vehicle WHERE VIN = :vin LIMIT 1"), {"vin": VIN}).first()
    if not vehicle_exists:
        raise HTTPException(status_code=404, detail="Vehicle with VIN not found")

    notice_exists = db.execute(text("SELECT 1 FROM Notice WHERE NID = :nid LIMIT 1"), {"nid": NID}).first()
    if not notice_exists:
        raise HTTPException(status_code=404, detail="Violation with NID not found")

    try:
        db.execute(text("UPDATE Notice SET Date = :violation_date, Time = :violation_time, Location = :location WHERE NID = :nid"), {"violation_date": violation_date, "violation_time": violation_time, "location": location, "nid": NID})
        db.execute(text("UPDATE Commits SET DLNum = :dl_num WHERE NID = :nid"), {"dl_num": DLNum, "nid": NID})
        db.execute(text("UPDATE Involves SET VIN = :vin WHERE NID = :nid"), {"vin": VIN, "nid": NID})
        db.execute(text("UPDATE Issues SET PID = :pid WHERE NID = :nid"), {"pid": PID, "nid": NID})
        db.execute(text("UPDATE NoticeVio SET VioCode = :vio_code, Notes = :notes WHERE NID = :nid"), {"vio_code": vioCode, "notes": notes, "nid": NID})
        db.execute(text("UPDATE NoticeAction SET ActCode = :act_code WHERE NID = :nid"), {"act_code": actCode, "nid": NID})

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating violation: {str(e)}")

    return {"message": "Violation updated successfully!"}


async def delete_violation(db: Session, NID: int):
    notice_exists = db.execute(text("SELECT 1 FROM Notice WHERE NID = :nid LIMIT 1"), {"nid": NID}).first()
    if not notice_exists:
        raise HTTPException(status_code=404, detail="Violation with NID not found")

    try:
        db.execute(text("DELETE FROM Notice WHERE NID = :nid"), {"nid": NID})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting violation: {str(e)}")

    return {"message": "Violation deleted successfully!"}

async def add_violation(db: Session, violation_date: date, violation_time: time, location: str, DLNum: str, PID: int, VIN: str, vioCode: str, notes: str, actCode: str):

    person_exists = db.execute(text("SELECT 1 FROM Person WHERE DLNum = :dl_num LIMIT 1"), {"dl_num": DLNum}).first()
    if not person_exists:
        raise HTTPException(status_code=404, detail="Person with DLNum not found")

    officer_exists = db.execute(text("SELECT 1 FROM Officer WHERE PID = :pid LIMIT 1"), {"pid": PID}).first()
    if not officer_exists:
        raise HTTPException(status_code=404, detail="Officer with PID not found")

    vehicle_exists = db.execute(text("SELECT 1 FROM Vehicle WHERE VIN = :vin LIMIT 1"), {"vin": VIN}).first()
    if not vehicle_exists:
        raise HTTPException(status_code=404, detail="Vehicle with VIN not found")

    try:
        result = db.execute(text("INSERT INTO Notice (Date, Time, Location) VALUES (:date, :time, :location)"), {"date": violation_date, "time": violation_time, "location": location})
        notice_id = result.lastrowid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding notice: {str(e)}")

    try:
        db.execute(text("INSERT INTO Commits (DLNum, NID) VALUES (:dl_num, :nid)"), {"dl_num": DLNum, "nid": notice_id})
        db.execute(text("INSERT INTO Involves (NID, VIN) VALUES (:nid, :vin)"), {"nid": notice_id, "vin": VIN})
        db.execute(text("INSERT INTO Issues (NID, PID) VALUES (:nid, :pid)"), {"nid": notice_id, "pid": PID})
        db.execute(text("INSERT INTO NoticeVio (NID, ItemID, VioCode, Notes) VALUES (:nid, 1, :vio_code, :notes)"), {"nid": notice_id, "vio_code": vioCode, "notes": notes})
        db.execute(text("INSERT INTO NoticeAction (NID, ActCode) VALUES (:nid, :act_code)"), {"nid": notice_id, "act_code": actCode})

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding violation: {str(e)}")

    return {"message": "Violation added successfully!"}