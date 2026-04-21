from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.lives import Lives
from app.crud.lives import get_lives, create_lives

router = APIRouter(prefix="/lives", tags=["lives"])

@router.get("/{PersonID}/{AddressNumber}/{AddressZipCode}", response_model=Lives)
async def get_lives_by_id(PersonID: int, AddressNumber: int, AddressZipCode: str, db: Session = Depends(get_db)):
    lives = await get_lives(db, PersonID, AddressNumber, AddressZipCode)
    if lives is None:
        raise HTTPException(status_code=404, detail="Lives not found")
    return lives

@router.post("/", response_model=Lives)
async def create_new_lives(lives: Lives, db: Session = Depends(get_db)):
    return await create_lives(db, lives)