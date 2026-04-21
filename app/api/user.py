from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema.user import User
from app.crud.user import get_user as crud_get_user, create_user as crud_create_user, get_user_by_username as crud_get_user_by_username
from app.db.session import get_db  

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{UserID}", response_model=User)
async def get_user(UserID: int, db: Session = Depends(get_db)):
    user = await crud_get_user(db, UserID)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/by-username/{Username}", response_model=User)
async def get_user_by_username(Username: str, db: Session = Depends(get_db)):
    user = await crud_get_user_by_username(db, Username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User)
async def create_user(user: User, db: Session = Depends(get_db)):
    existing_user = await crud_get_user_by_username(db, user.Username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return await crud_create_user(db, user)

