from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
import jwt

hashing = CryptContext(schemes=["argon2"], deprecated="auto")

SECRET_KEY = "76d8713fda6016ae5c64e42b1b034bd0b05f120def5706c840583553945c32c5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def getPasswordHash(password):
    return hashing.hash(password)

def verifyPassword(plain_password, hashed_password):
    return hashing.verify(plain_password, hashed_password)

def createAccessToken(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt