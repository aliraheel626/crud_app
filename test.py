from pydantic import BaseModel



class UserCreate(BaseModel):
    username: str
    password: str
    email:str
    name:str
    age:int


user = UserCreate(username="ali", password="ali", email="ali@email.com", name="ali", age=12)
print(user.model_dump())
print(*user.model_dump())

def test(username, password, email, name, age):
    print(username, password, email, name, age)
test(username='ali', email ='ali@email.com', name='ali', age=12, password='ali')
test(**user.model_dump())
