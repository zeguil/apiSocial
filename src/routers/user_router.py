import bcrypt
from typing import List
from schemas.user import *
from decouple import config
from models.user import User
from config.database import Session
from config.dependencies import get_db
from utils.email_utils import send_email
from itsdangerous import URLSafeTimedSerializer
from controllers.userController import UserController
from fastapi import APIRouter, Depends, HTTPException
from utils.user_utils import generate_reset_token, valid_password


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

@userRouter.get("/active/{activation_token}", status_code=200)
def activate_account(activation_token: str, db: Session = Depends(get_db)):
    user: User = db.query(User).filter_by(token=activation_token).first()
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
    
    db.commit()
    
    return {"message": "Account activated successfully"}

@userRouter.post("/forgotpassword")
def forgot_password(email_request: EmailRequest, db: Session = Depends(get_db)):
    print("entrei")
    # Verifica se o email fornecido existe no banco
    user: User = db.query(User).filter_by(email=email_request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Gera um token de redefinição de senha
    reset_token = generate_reset_token()

    # Salva o token no banco
    user.token = reset_token
    db.commit()

    # Envia o e-mail de redefinição de senha para o usuário
    send_email(email=user.email, token=reset_token, type=2, name= user.username)

    return {"message": "Password reset email sent"}


@userRouter.post("/resetpassword")
def reset_password(reset_request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # Verifica se o token de redefinição de senha é válido
    user: User = db.query(User).filter_by(token=reset_request.token).first()
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
    db.commit()

    return {"message": "Password reset successful"}