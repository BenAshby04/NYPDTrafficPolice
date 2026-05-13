from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_db import init_db
from app.api import actionCode, address, assigned, detatchment, district, lives, officer, owns, partOf, person, registered, token, user, vehicle, violation, violationCode, userPerson

app = FastAPI()

init_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500",
                   "http://localhost:5500",
                   "http://127.0.0.1:3000",
                   "http://localhost:3000",
                   "http://127.0.0.1:8000",
                   "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the NYPD Traffic Police API!"}

app.include_router(actionCode.router)
app.include_router(address.router)
app.include_router(assigned.router)
app.include_router(detatchment.router)
app.include_router(district.router)
app.include_router(lives.router)
app.include_router(officer.router)
app.include_router(owns.router)
app.include_router(partOf.router)
app.include_router(person.router)
app.include_router(registered.router)
app.include_router(token.router)
app.include_router(user.router)
app.include_router(vehicle.router)
app.include_router(violation.router)
app.include_router(violationCode.router)
app.include_router(userPerson.router)