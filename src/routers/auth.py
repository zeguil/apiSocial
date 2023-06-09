from typing import List
from schemas.user import *
from config.database import Session
from fastapi import APIRouter, Depends
from config.dependencies import get_db
from controllers.userController import UserController


authRouter = APIRouter(prefix='/user', tags=['Usuários'] )