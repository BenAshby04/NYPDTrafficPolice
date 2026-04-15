from fastapi import FastAPI, HTTPException, Depends, status
from datetime import date, datetime, time
from pydantic import BaseModel
from typing import List, Optional
from dbConn import conn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the NYPD API!"}


@app.get("/violations")
async def get_violations():
    curr = conn.cursor()
    curr.execute("SELECT * FROM ViolationCode")
    violations = curr.fetchall()
    curr.close()
    return {"violations": violations}

@app.get("/violations/{DLNum}")
async def get_violations_by_dlnum(DLNum: str):
    curr = conn.cursor()
    curr.callproc("NYPD.GetCiviData", (DLNum,))
    violations = curr.fetchall()
    curr.close()
    if len(violations) == 0:
        raise HTTPException(status_code=404, detail="No violations found for the provided DLNum.")

    return {"violations": violations}


@app.get("/officer/{PID}")
async def get_officer_info(PID: int):
    curr = conn.cursor()
    query = "SELECT * FROM Officer WHERE PID = %s"
    curr.execute(query, (PID,))
    officer_info = curr.fetchall()
    curr.close()
    if len(officer_info) == 0:
        raise HTTPException(status_code=404, detail="No officer found with the provided PID")
    return {"officer_info": officer_info}




@app.post("/add_vehicle/{VIN}/{license_plate}/{state_plate}/{year}/{make}")
async def add_vehicle(VIN: str, license_plate: str, state_plate: str, year: int, make: str):
    curr = conn.cursor()
    query = "INSERT INTO Vehicle (VIN, LPlate, StatePlate, Year, Make) VALUES (%s, %s, %s, %s, %s)"
    try:
        curr.execute(query, (VIN, license_plate, state_plate, year, make))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error adding vehicle: " + str(e))
    curr.close()
    return {"message": "Vehicle added successfully!"}


@app.post("/add_violation/{date}/{time}/{location}/{DLNum}/{PID}/{VIN}/{vioCode}/{notes}/{actCode}")
async def add_violation(date: date, time: time, location: str, DLNum: str, PID: int, VIN: str, vioCode: str, notes: str, actCode: str):
    curr = conn.cursor()
    #Do notice query first to get the notice_id for the related tables
    curr.execute("SELECT DLNum FROM Person WHERE DLNum = %s", (DLNum,))
    if len(curr.fetchall()) == 0:
        raise HTTPException(status_code=404, detail="Person with DLNum not found")
    curr.execute("SELECT PID FROM Officer WHERE PID = %s", (PID,))
    if len(curr.fetchall()) == 0:
        raise HTTPException(status_code=404, detail="Officer with PID not found")
    curr.execute("SELECT VIN FROM Vehicle WHERE VIN = %s", (VIN,))
    if len(curr.fetchall()) == 0:
        raise HTTPException(status_code=404, detail="Vehicle with VIN not found")    

    noticeQuery = "INSERT INTO Notice (Date, Time, Location) VALUES (%s, %s, %s)"
    try:
        curr.execute(noticeQuery, (date, time, location))
        notice_id = curr.lastrowid
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error adding notice: " + str(e))
    
    commitQuery = "INSERT INTO Commits (DLNum, NID) VALUES (%s, %s)"
    involvesQuery = "INSERT INTO Involves (NID, VIN) VALUES (%s, %s)"
    issuesQuery = "INSERT INTO Issues(NID,PID) VALUES (%s, %s)"
    noticeVioQuery = "INSERT INTO NoticeVio (NID, ItemID, VioCode, Notes) VALUES (%s, 1, %s, %s)"
    noticeActionQuery = "INSERT INTO NoticeAction (NID,ActCode) VALUES (%s, %s)"
    try:
        curr.execute(commitQuery, (DLNum, notice_id))
        curr.execute(involvesQuery, (notice_id, VIN))
        curr.execute(issuesQuery, (notice_id, PID))
        curr.execute(noticeVioQuery, (notice_id, vioCode, notes))
        curr.execute(noticeActionQuery, (notice_id, actCode))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error adding violation: " + str(e))
    curr.close()
    return {"message": "Violation added successfully!"}

@app.post("/add_officer/{PID}/{first_name}/{last_name}")
async def add_officer(PID: int, first_name: str, last_name: str):
    curr = conn.cursor()
    query = "INSERT INTO Officer (PID, FName, LName) VALUES (%s, %s, %s)"
    try:
        curr.execute(query, (PID, first_name, last_name))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error adding officer: " + str(e))
    curr.close()
    return {"message": "Officer added successfully!"}


@app.put("/update_officer/{PID}/{first_name}/{last_name}")
async def update_officer(PID: int, first_name: str, last_name: str):
    curr = conn.cursor()
    query = "UPDATE Officer SET FName = %s, LName = %s WHERE PID = %s"
    try:
        curr.execute(query, (first_name, last_name, PID))
        conn.commit()
        if curr.rowcount == 0:
            raise HTTPException(status_code=404, detail="Officer with PID not found")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=404, detail="Error updating officer: " + str(e))
    curr.close()
    return {"message": "Officer updated successfully!"}

@app.put("/update_vehicle/{VIN}/{license_plate}/{state_plate}/{year}/{make}")
async def update_vehicle(VIN: str, license_plate: str, state_plate: str, year: int, make: str):
    curr = conn.cursor()
    query = "UPDATE Vehicle SET LPlate = %s, StatePlate = %s, Year = %s, Make = %s WHERE VIN = %s"
    try:
        curr.execute(query, (license_plate, state_plate, year, make, VIN))
        conn.commit()
        if curr.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehicle with VIN not found")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error updating vehicle: " + str(e))
    curr.close()
    return {"message": "Vehicle updated successfully!"}

@app.put("/update_violation/{NID}/{date}/{time}/{location}/{DLNum}/{PID}/{VIN}/{vioCode}/{notes}/{actCode}")
async def update_violation(NID: int, date: date, time: time, location: str, DLNum: str, PID: int, VIN: str, vioCode: str, notes: str, actCode: str):
    curr = conn.cursor()
    #Do notice query first to get the notice_id for the related tables
    curr.execute("SELECT DLNum FROM Person WHERE DLNum = %s", (DLNum,))
    if len(curr.fetchall()) == 0:
        raise HTTPException(status_code=404, detail="Person with DLNum not found")
    curr.execute("SELECT PID FROM Officer WHERE PID = %s", (PID,))
    if len(curr.fetchall()) == 0:
        raise HTTPException(status_code=404, detail="Officer with PID not found")
    curr.execute("SELECT VIN FROM Vehicle WHERE VIN = %s", (VIN,))
    if len(curr.fetchall()) == 0:
        raise HTTPException(status_code=404, detail="Vehicle with VIN not found")    

    curr.execute("SELECT NID FROM Notice WHERE NID = %s", (NID,))
    if len(curr.fetchall()) == 0:
        raise HTTPException(status_code=404, detail="Violation with NID not found")

    noticeQuery = "UPDATE Notice SET Date = %s, Time = %s, Location = %s WHERE NID = %s"
    try:
        curr.execute(noticeQuery, (date, time, location, NID))
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error updating notice: " + str(e))
    
    commitQuery = "UPDATE Commits SET DLNum = %s WHERE NID = %s"
    involvesQuery = "UPDATE Involves SET VIN = %s WHERE NID = %s"
    issuesQuery = "UPDATE Issues SET PID = %s WHERE NID = %s"
    noticeVioQuery = "UPDATE NoticeVio SET VioCode = %s, Notes = %s WHERE NID = %s"
    noticeActionQuery = "UPDATE NoticeAction SET ActCode = %s WHERE NID = %s"
    try:
        curr.execute(commitQuery, (DLNum, NID))
        curr.execute(involvesQuery, (VIN, NID))
        curr.execute(issuesQuery, (PID, NID))
        curr.execute(noticeVioQuery, (vioCode, notes, NID))
        curr.execute(noticeActionQuery, (actCode, NID))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error updating violation 2: " + str(e))
    curr.close()
    return {"message": "Violation updated successfully!"}


@app.delete("/delete_officer/{PID}")
async def delete_officer(PID: int):
    curr = conn.cursor()
    query = "DELETE FROM Officer WHERE PID = %s"
    try:
        curr.execute(query, (PID,))
        conn.commit()
        if curr.rowcount == 0:
            raise HTTPException(status_code=404, detail="Officer with PID not found")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error deleting officer: " + str(e))
    curr.close()
    return {"message": "Officer deleted successfully!"}

@app.delete("/delete_vehicle/{VIN}")
async def delete_vehicle(VIN: str):
    curr = conn.cursor()
    query = "DELETE FROM Vehicle WHERE VIN = %s"
    try:
        curr.execute(query, (VIN,))
        conn.commit()
        if curr.rowcount == 0:
            raise HTTPException(status_code=404, detail="Vehicle with VIN not found")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error deleting vehicle: " + str(e))
    curr.close()
    return {"message": "Vehicle deleted successfully!"}

@app.delete("/delete_violation/{NID}")
async def delete_violation(NID: int):
    curr = conn.cursor()
    query = "DELETE FROM Notice WHERE NID = %s"
    try:
        curr.execute(query, (NID,))
        conn.commit()
        if curr.rowcount == 0:
            raise HTTPException(status_code=404, detail="Violation with NID not found")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Error deleting violation: " + str(e))
    curr.close()
    return {"message": "Violation deleted successfully!"}   
