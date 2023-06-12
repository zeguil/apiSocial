from pydantic import BaseModel
import datetime

class ProfileBase(BaseModel):
    full_name: str
    bio: str


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileRequest(ProfileBase):
    full_name: str
    bio: str
    

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True