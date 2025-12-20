from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///test.db")

#dependency
def get_db():
    with Session(bind=engine, autocommit=False) as session:
        yield session
    print('session closed')
