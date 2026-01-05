from sqlmodel import SQLModel
from sqlmodel import Field
from datetime import datetime
# CREATE TABLE User (
#     username int,
#     password varchar(255),
#     email varchar(255),
#     name varchar(255),
#     age int
# );
class User(SQLModel,table=True):
    __tablename__ = "user"
    id:int = Field(default=None, primary_key=True)
    username: str
    password: str
    email:str

class Chat(SQLModel,table=True):
    __tablename__ = "chat"
    id:int = Field(default=None, primary_key=True)
    user_id:int = Field(foreign_key="user.id")
    name: str

class Message(SQLModel,table=True):
    __tablename__ = "message"
    id:int = Field(default=None, primary_key=True)
    chat_id:int = Field(foreign_key="chat.id")
    user_id:int = Field(foreign_key="user.id")
    content: str
    role: str

class Session(SQLModel,table=True):
    __tablename__ = "session"
    id:int = Field(default=None, primary_key=True)
    user_id:int = Field(foreign_key="user.id")
    created_at: datetime = Field(default=datetime.now())
    expires_after: int = Field(default=3600)


