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


class UserController():
    def __init__(self, db:Session):
        self.db = db

    def create_user(self, user: UserRequest):
        validate_user_data(user)
        try:
            existing_user: User = self.db.query(User).filter(or_(User.username == user.username, User.email == user.email)).first()
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

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            send_email(token=activation_token, name=user.username, email=user.email, type=1)

            return new_user
        except SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")