from fastapi import FastAPI
from app.models import *
from sqlmodel import SQLModel
from app.database import engine
SQLModel.metadata.create_all(engine)

app = FastAPI()


