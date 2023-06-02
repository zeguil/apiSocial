from pydantic import BaseModel
from pydantic.types import Optional

class UserRequest(BaseModel):
    username: str
    password: str
    email: str
    # is_admin: bool = False

class UserResponse(BaseModel):
    username: str
    email: str
    
    class Config:
        orm_mode = True


class UserPassword(BaseModel):
    password: str
    confirm_password: str
    new_password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]

class EmailRequest(BaseModel):
    email: str


class NewPasswordRequest(BaseModel):
    old_passwod: str
    new_password: str
    confirm_password: str

class ForgotPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str