from fastapi import FastAPI
from app.models import *
from sqlmodel import SQLModel
from app.database import engine, get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import User
from app.routes.user_routes import router as user_router
from app.routes.chat_routes import router as chat_router
import app.database



app = FastAPI()

app.include_router(user_router)
app.include_router(chat_router)




