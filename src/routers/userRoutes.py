from typing import List
from schemas.user import *
from config.database import Session
from fastapi import APIRouter, Depends
from config.dependencies import get_db
from controllers.userController import UserController
from utils.auth import logged_user

userRouter = APIRouter(prefix='/user', tags=['Usuários'] )

# Listar Usuários
@userRouter.get("/", response_model=List[UserResponse], status_code=200)
def list_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    users = UserController(db).list_users()
    return users

# Listar Usuário Pelo ID
@userRouter.get("/{id_user}", response_model=UserResponse, status_code=200)
def get_user_by_id(id_user: int, db: Session = Depends(get_db)) -> UserResponse:
    user = UserController(db).list_user(id_user)
    return user

# Criar Usuário
@userRouter.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserRequest, db: Session = Depends(get_db)) -> UserResponse:
    new_user = UserController(db).create_user(user)
    return new_user

# Atualiza Dados do Usuário
@userRouter.put("/{id_user}", response_model=UserResponse, status_code=200)
def update_user(id_user: int, user_update: UserUpdate, db: Session = Depends(get_db)) -> UserResponse:
   user =  UserController(db).update_user(id_user, user_update=user_update)
   return user


@userRouter.delete("/{id_user}", status_code=204)
def delete_user(id_user: int, db: Session = Depends(get_db)) -> None:
    UserController(db).delete_user(id_user)

