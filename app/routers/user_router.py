from fastapi import APIRouter
from typing import List


userRouter = APIRouter(prefix='/user')


@userRouter.get("/")
def list_users() -> List:
    return [
            {"id": 1, "user": "Jose"},
            {"id": 2, "user": "Lucas"},
            ]
