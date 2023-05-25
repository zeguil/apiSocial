from fastapi import APIRouter, Depends, HTTPException
from config.database import Session
from config.dependencies import get_db
from typing import List
from pydantic import BaseModel
from models.user import User
import bcrypt

class UserRequest(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class UserResponse(BaseModel):
    username: str
    
    class Config:
        orm_mode = True

userRouter = APIRouter(prefix='/user', )


#! Get all users 
@userRouter.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)) -> List[UserResponse]:

    users = db.query(User).all()

    return users


#! Get User by your id
@userRouter.get("/" ,response_model=UserResponse, status_code=200)
def list_user_by_id(id_user: int, db: Session = Depends(get_db)) -> UserResponse:

    user = db.query(User).get(id_user)

    if not user:
        raise HTTPException(status_code=404, detail="item not found")

    return user

#! Create User
@userRouter.post("/", response_model= UserResponse, status_code=201)
def create_user(user: UserRequest, db: Session = Depends(get_db)) -> UserResponse:

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        username=user.username,
        password=hashed_password.decode('utf-8')
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#! Update User
@userRouter.put("/{id_user}", response_model=UserResponse,  status_code=200)
def update_user(id_user: int, user_request: UserRequest, db: Session = Depends(get_db)) -> UserResponse:
    
    user: User =  db.query(User).get(id_user)
    # Campos a serem atualizados
    user.username = user_request.username
    user.password = user_request.password
    user.is_admin = user_request.is_admin

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#! Delete User
@userRouter.delete("/{id_user}", status_code=204)
def delete_user(id_user: int, db: Session = Depends(get_db)) -> None:

    user = db.query(User).get(id_user)
    if user:
        db.delete(user)
        db.commit()

        return {"msg": "deleted user"}
    
