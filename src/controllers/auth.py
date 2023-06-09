from random import randint
from fastapi import status, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.auth import Password, Login, LoginSuccess, ForgotPassword, ResetPassword
from utils.hash import verify_hash, generate_hash, encoder, decoder
from utils.access_token import create_access_token, verify_acess_token

from jose import JWTError

class AuthController():
    def __init__(self, db: Session):
        self.db = db

    def token(self, login_data: Login):
        user = self.db.query(User).filter_by(username= login_data.username).first()

        if not user:
            raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
        
        valid_password = verify_hash(login_data.password, user.password)
        if not valid_password:
            raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

        # Gerar Token JWT
        new_token = create_access_token({'sub': user.username})
        message = "Usuário fez login com sucesso"
        return LoginSuccess(user=user, access_token=new_token, message=message)
    
    def get_by_username(self, username) -> User:
        query = select(User).where(
            User.username == username)
        return self.db.execute(query).scalars().first()
    
    def validate_code(self, code, email):
        
        user = self.db.query(User).filter_by(email=email).first()
        
        if user:
            if user.email == email and user.code == code:
                print(f"encontrei o usuario {email}")   
                user.code = str(randint(100100, 998989))
                self.db.commit()
                return {"msg": "Código válido"}
            else:
                print("Email e codigo não coincidem")
                raise HTTPException(status_code=401, detail="Código inválido ")
        else:
            print("User não encontrado")
            raise HTTPException(status_code=401, detail="Código inválido ")
            
    def reset_password(self, psw: ResetPassword):
        
        user = self.db.query(User).filter_by(email=psw.email).first()
        
        
        if  psw.new_password == psw.confirm_password:
            user.password = generate_hash(psw.new_password)
            self.db.commit()
            return "Senha alterada com sucesso"

        raise HTTPException(status_code=400, detail="As senhas não são iguais")