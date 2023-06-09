
import bcrypt
from typing import List
from schemas.user import *
from decouple import config
from models.user import User
from config.database import Session
from config.dependencies import get_db
from utils.email_utils import send_email
from itsdangerous import URLSafeTimedSerializer
from controllers.userActionController import UserActionController
from fastapi import APIRouter, Depends, HTTPException
from utils.user_utils import generate_reset_token, valid_password

userActions = APIRouter(prefix='/account', tags=['Usuários'] )

@userActions.get("/active/{activation_token}", status_code=200)
def activate_account(activation_token: str, db: Session = Depends(get_db)):
    return UserActionController(db).activate_account(activation_token)

@userActions.post("/forgotpassword")
def forgot_password(email_request: EmailRequest, db: Session = Depends(get_db)):
   return UserActionController(db).forgot_password(email_request)


@userActions.post("/resetpassword")
def reset_password(reset_request: ForgotPasswordRequest, db: Session = Depends(get_db)):
   return UserActionController(db).reset_password(reset_request)