from typing import List
from schemas.profile import *
from config.database import Session
from fastapi import APIRouter, Depends
from config.dependencies import get_db
from utils.auth import logged_user
from schemas.auth import *
from schemas.profile import *
from controllers.profileController import ProfileController

profileRouter = APIRouter(prefix="/profile", tags=['Profile'])


@profileRouter.post("")
def create_profile(profile: ProfileRequest, user: SimpleUser = Depends(logged_user), db : Session = Depends(get_db)):
    new_user = ProfileController(db).create_profile(profile)
    return new_user