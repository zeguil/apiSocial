import cryptocode
import bcrypt
from random import randint
from decouple import config
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])


def generate_hash(text):
    return pwd_context.hash(text)


def verify_hash(text, hashed_text):
    return bcrypt.checkpw(text.encode('utf-8'), hashed_text.encode('utf-8'))

def encoder(token=''):
    
    if token:
        str_encoded = cryptocode.encrypt(str(token), config('SECRET_KEY'))
        return str_encoded
    
    str_encoded = cryptocode.encrypt(str(randint(100001, 999999)), config('SECRET_KEY'))
    return str_encoded

def decoder(key):
    str_decoded = cryptocode.decrypt(key, config('SECRET_KEY'))
    return str_decoded