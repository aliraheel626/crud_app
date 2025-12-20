from sqlmodel import SQLModel
from sqlmodel import Field
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
    username: int
    password: str
    email:str
    name:str
    age:int


