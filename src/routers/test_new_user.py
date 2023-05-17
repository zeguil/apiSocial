from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, declarative_base
from ..config.dependencies import get_db
import bcrypt
from pydantic import BaseModel

app = FastAPI()
Base = declarative_base()


class UserRequest(BaseModel):
    id: int
    username: str
    password: str

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)

    @classmethod
    def create_user(cls, session: Session, user_request: UserRequest):
        hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), bcrypt.gensalt())

        user = cls(username=user_request.username, password=hashed_password.decode('utf-8'))
        session.add(user)
        session.commit()


@app.post("/users")
def create_user(user_request: UserRequest, session: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), bcrypt.gensalt())

    user = User(username=user_request.username, password=hashed_password.decode('utf-8'))
    session.add(user)
    session.commit()

    return {"message": "Usuário criado com sucesso!"}