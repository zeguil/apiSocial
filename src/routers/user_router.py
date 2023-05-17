from fastapi import APIRouter, Depends
from config.database import Session
from config.dependencies import get_db
from typing import List
from pydantic import BaseModel
from models.user import User

class UserRequest(BaseModel):
    username: str
    password: str
    

class UserResponse(BaseModel):
    username: str
    
    class Config:
        orm_mode = True

userRouter = APIRouter(prefix='/user')


@userRouter.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)) -> List[UserRequest]:

    users = db.query(User).all()

    return users


  

@userRouter.post("/", response_model= UserResponse, status_code=201)
def create_user(user: UserRequest, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user