from fastapi import APIRouter, Depends, HTTPException
from config.database import Session
from config.dependencies import get_db
from typing import List
from pydantic import BaseModel
from sqlalchemy import or_
from models.user import User
from utils.user_utils import (validate_user_data)
import bcrypt

class UserRequest(BaseModel):
    username: str
    password: str
    email: str
    is_admin: bool = False

class UserResponse(BaseModel):
    username: str
    email: str
    
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

    # Verifica se o usuário existe no banco
    if not user:
        raise HTTPException(status_code=404, detail="item not found")

    return user

#! Create User
@userRouter.post("/", response_model= UserResponse, status_code=201)
def create_user(user: UserRequest, db: Session = Depends(get_db)) -> UserResponse:

    validate_user_data(user)
    
    existing_user = db.query(User).filter(or_(User.username == user.username, User.email == user.email)).first()
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=409, detail="Username already in use")
        else:
            raise HTTPException(status_code=409, detail="Email already in use")
    
    # Criptografa a senha antes de salvar no banco
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        username=user.username,
        password=hashed_password.decode('utf-8'),
        email = user.email
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
    
