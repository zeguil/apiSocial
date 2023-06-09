import os
from datetime import datetime, timedelta
from jose import jwt
from decouple import config

# JOSE Config vars
SECRET_KEY = 'P@ssw0rd!23QuickLink'
ALGORITHM = 'HS256'
EXPIRES_IN_MINUTES = 600

def create_access_token(data_base: dict):
    data = data_base.copy()
    expires = datetime.utcnow() + timedelta(minutes=int(EXPIRES_IN_MINUTES))

    data.update({'exp': expires})

    token_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return token_jwt

def verify_acess_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')
