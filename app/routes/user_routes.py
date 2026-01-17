from app.database import get_db
from app.models import User, Session
from app.schemas import UserRegister, UserLogin
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session as DatabaseSession
from sqlalchemy import select
from fastapi import Cookie
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDatabaseSession
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from typing import Annotated

router = APIRouter()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_hash = PasswordHash.recommended()
class Token(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class UserCreate(BaseModel):
    username: str
    password: str
    email:str


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)

#dependency
async def get_current_user(db:AsyncDatabaseSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        if payload.get("exp") < datetime.now(timezone.utc).timestamp():
            raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


@router.post("/register")
async def create_user(user: UserRegister, db: AsyncDatabaseSession = Depends(get_db)):
    user = User(**user.model_dump())
    user.password = get_password_hash(user.password)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
async def login(user_login: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncDatabaseSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == user_login.username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "exp": datetime.now(timezone.utc) + access_token_expires},
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return user
    


