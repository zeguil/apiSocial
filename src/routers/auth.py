from typing import List
from schemas.auth import *
from config.database import Session
from fastapi import APIRouter, Depends
from config.dependencies import get_db
from utils.auth import logged_user
from controllers.auth import AuthController


authRouter = APIRouter(prefix='/auth', tags=['Autênticação'] )



@authRouter.post('/token', response_model=LoginSuccess)
async def sing_in(login_data: Login, db: Session = Depends(get_db)):
    return AuthController(db).token(login_data)

@authRouter.post('/logout')
async def sing_out(user: SimpleUser = Depends(logged_user), db: Session = Depends(get_db)):
    return AuthController(db)

@authRouter.get('/me', response_model=SimpleUser)
async def me(user: SimpleUser = Depends(logged_user), db: Session = Depends(get_db)):
    return user