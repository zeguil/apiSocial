from fastapi import APIRouter, Response
from typing import List
from pydantic import BaseModel

class UserRequest(BaseModel):
    id: int
    user: str
    age: int

class UserResponse(BaseModel):
    
    user: str
    age: int

userRouter = APIRouter(prefix='/user')


@userRouter.get("/", response_model=List[UserResponse])
def list_users() -> List[UserRequest]:
    return [
            UserResponse(id=1, user="Jose", age=23),
            UserResponse(id=2, user= "Lucas", age=27),
            ]


@userRouter.post("/", response_model= UserResponse, status_code=201)
def create_user(conta: UserRequest):
    return UserRequest(
        id= conta.id,
        user= conta.user,
        age= conta.age
    )