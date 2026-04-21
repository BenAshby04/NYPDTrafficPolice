from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from app.core.security import SECRET_KEY, ALGORITHM,createAccessToken
from app.schema.user import User
from app.schema.token import TokenData, Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

