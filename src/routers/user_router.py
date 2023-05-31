from fastapi import APIRouter, Depends, HTTPException
from config.database import Session
from config.dependencies import get_db
from typing import List
from decouple import config
from schemas.user import *
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from utils.user_utils import validate_user_data
from utils.email_utils import send_email
import bcrypt
from logs.logger import logger
from itsdangerous import URLSafeTimedSerializer

userRouter = APIRouter(prefix='/user', tags=['Usuários'] )

# Listar Usuários
@userRouter.get("/", response_model=List[UserResponse], status_code=200)
def list_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    users = db.query(User).all()
    return users

# Listar Usuário Pelo ID
@userRouter.get("/{id_user}", response_model=UserResponse, status_code=200)
def get_user_by_id(id_user: int, db: Session = Depends(get_db)) -> UserResponse:
    try:
        user: User = db.query(User).get(id_user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Criar Usuário
@userRouter.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserRequest, db: Session = Depends(get_db)) -> UserResponse:
    validate_user_data(user)
    try:
        existing_user: User = db.query(User).filter(or_(User.username == user.username, User.email == user.email)).first()
        # verifica se usrário ou email estão em uso
        if existing_user:
            if existing_user.username == user.username:
                raise HTTPException(status_code=409, detail="Username already in use")
            else:
                raise HTTPException(status_code=409, detail="Email already in use")
        # criptografa a senha
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        serializer = URLSafeTimedSerializer(config('SECRET_KEY'))

        activation_token = serializer.dumps(user.email, salt="activation")

        new_user = User(
            username=user.username,
            password=hashed_password.decode('utf-8'),
            email=user.email,
            token=activation_token
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        send_email(token=activation_token, name=user.username, email=user.email)

        return new_user
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Atualiza Dados do Usuário
@userRouter.put("/{id_user}", response_model=UserResponse, status_code=200)
def update_user(id_user: int, user_update: UserUpdate, db: Session = Depends(get_db)) -> UserResponse:
    try:
        user: User = db.query(User).get(id_user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user_update.username:
            user.username = user_update.username
        
        if user_update.email:
            user.email = user_update.email
        
        db.commit()
        db.refresh(user)

        updated_user_response_data = {}
        if user.username:
            updated_user_response_data["username"] = user.username
        if user.email:
            updated_user_response_data["email"] = user.email
        
        updated_user_response = UserResponse(**updated_user_response_data)
        
        return updated_user_response
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@userRouter.delete("/{id_user}", status_code=204)
def delete_user(id_user: int, db: Session = Depends(get_db)) -> None:
    try:
        user: User = db.query(User).get(id_user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(user)
        db.commit()
    except SQLAlchemyError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@userRouter.get("/active/{activation_token}", status_code=200)
def activate_account(activation_token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(token=activation_token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Activation token not found")
    
    if user.is_active:
        raise HTTPException(status_code=400, detail="Account already activated")
    
    # Ative a conta do usuário
    user.is_active = True
    user.token = None  # Remova o token de ativação
    
    db.commit()
    
    return {"message": "Account activated successfully"}