from app.database import get_db
from app.models import User, Session
from app.schemas import UserRegister, UserLogin
from fastapi import APIRouter, Depends, Response


router = APIRouter()

@router.post("/register")
def create_user(user: UserRegister, db:Session = Depends(get_db)):
    user = User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(user_login: UserLogin, response:Response, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.password == user_login.password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    session = Session(user_id=user.id)
    db.add(session)
    db.commit()
    db.refresh(session)
    response.set_cookie(key="session_id", value=session.id)
    return session


@router.get("/me")
def me(db:Session = Depends(get_db)):
    pass

