from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.userPerson import UserPerson
from app.crud.userPerson import create_link, delete_link, get_link_by_dlnum, get_link_by_user

router = APIRouter(prefix="/user-person", tags=["user-person"])

@router.get("/by-user/{UserID}", response_model=UserPerson)
async def get_by_user(UserID: int, db: Session = Depends(get_db)):
    link = await get_link_by_user(db, UserID)
    if link is None:
        raise HTTPException(status_code=404,detail="Link not found for this user")
    return link

@router.get('/by-dlnum/{DLNum}', response_model=UserPerson)
async def get_by_dlnum(DLNum: str, db: Session = Depends(get_db)):
    link = await get_link_by_dlnum(db, DLNum)
    if link is None:
        raise HTTPException(status_code=404, detail="Link is not found for this DL number")
    return link

@router.post('/', response_model=UserPerson)
async def create_new_link(link:UserPerson, db:Session = Depends(get_db)):
    return await create_link(db,link)

@router.delete("/{UserID}")
async def delete_link_by_user(UserID: int, db: Session = Depends(get_db)):
    return await delete_link(db, UserID)