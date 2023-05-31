from itsdangerous import URLSafeTimedSerializer
from decouple import config
import time

nome = "jose"

serializer = URLSafeTimedSerializer(config('SECRET_KEY'))

    
token1 = serializer.dumps(nome, salt="activation")
token2 = serializer.dumps(nome, salt="renew")

print(token1 == token2)