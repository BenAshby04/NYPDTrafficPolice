from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.db.session import get_db
from app.schema.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.crud.user import get_user_by_username
from app.core.security import verifyPassword, createAccessToken
from sqlalchemy.orm import Session


router = APIRouter(prefix="/token", tags=["token"])

@router.post("/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = get_user_by_username(db,form_data.username)
    if not user or not verifyPassword(form_data.password, user.HashedPassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = createAccessToken(data={"sub": user.Username})
    return Token(access_token=access_token, token_type="bearer")

