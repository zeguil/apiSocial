import bcrypt
from schemas.user import *
from sqlalchemy import or_
from decouple import config
from models.user import User
from logs.logger import logger
from fastapi import HTTPException
from config.database import Session
from utils.email_utils import send_email
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from itsdangerous import URLSafeTimedSerializer
from utils.user_utils import validate_user_data, generate_reset_token, valid_password

class UserActionController():

    def __init__(self, db:Session):
        self.db = db

    def activate_account(self, activation_token: str):
        user: User = self.db.query(User).filter_by(token=activation_token).first()
        if not user:
            raise HTTPException(status_code=404, detail="Activation token not found")
        
        if user.is_active:
            raise HTTPException(status_code=400, detail="Account already activated")
        
        serializer = URLSafeTimedSerializer(config('SECRET_KEY'))

        token = serializer.dumps(user.email, salt="renew")

        # Ative a conta do usuário
        user.is_active = True
        # Atualiza o token
        user.token = token  
        
        self.db.commit()
        
        return {"message": "Account activated successfully"}


    def forgot_password(self, email_request: EmailRequest):
        
        # Verifica se o email fornecido existe no banco
        user: User = self.db.query(User).filter_by(email=email_request.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Email not found")

        # Gera um token de redefinição de senha
        reset_token = generate_reset_token()

        # Salva o token no banco
        user.token = reset_token
        self.db.commit()

        # Envia o e-mail de redefinição de senha para o usuário
        send_email(email=user.email, token=reset_token, type=2, name= user.username)

        return {"message": "Password reset email sent"}



    def reset_password(self, reset_request: ForgotPasswordRequest):
        # Verifica se o token de redefinição de senha é válido
        user: User = self.db.query(User).filter_by(token=reset_request.token).first()
        if not user:
            raise HTTPException(status_code=404, detail="Invalid reset token")
        
        if reset_request.new_password != reset_request.confirm_password:
            raise HTTPException(status_code=400, detail="The passwords do not match")

        if not valid_password(reset_request.new_password):
            raise HTTPException(status_code=409, detail="Invalid reset password")
        
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        # Atualiza a senha do usuário com a nova senha fornecida
        user.password = hashed_password.decode('utf-8')
        user.token = None  # Limpa o token de redefinição de senha
        self.db.commit()

        return {"message": "Password reset successful"}