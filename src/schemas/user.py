from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class UserResponse(BaseModel):
    username: str


class UserPassword(BaseModel):
    password: str
    confirm_password: str
    new_password: str

class UserUpdate(BaseModel):
    username: str

