from app.database import get_db
from app.models import User, Session
from app.schemas import UserRegister, UserLogin
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session as DatabaseSession
from fastapi import Cookie
from fastapi import HTTPException

router = APIRouter()

#dependency
def get_current_user(db:DatabaseSession = Depends(get_db), session_id: int = Cookie(None)):
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=400, detail="Invalid session")
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid session")
    return user


@router.post("/register")
def create_user(user: UserRegister, db: DatabaseSession = Depends(get_db)):
    user = User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(user_login: UserLogin, response:Response, db: DatabaseSession = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.password == user_login.password:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    session = Session(user_id=user.id)
    db.add(session)
    db.commit()
    db.refresh(session)
    response.set_cookie(key="session_id", value=session.id)
    return session


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return user
    


