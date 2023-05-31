import re
from fastapi import HTTPException
from itsdangerous import URLSafeTimedSerializer
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from decouple import config
blacklist = []

def valid_password(senha):
    # Verificar se tem pelo menos 8 caracteres
    if len(senha) < 8:
        return False
    
    # Verificar se tem pelo menos 1 número
    if not re.search(r'\d', senha):
        return False
    
    # Verificar se tem pelo menos 1 letra maiúscula
    if not re.search(r'[A-Z]', senha):
        return False
    
    # A senha atende a todos os critérios
    return True

def valid_username(username):
    # Verifica se o campo não está vazio
    if not username:
        return False

    # Verifica o tamanho do nome de usuário
    if len(username) > 10:
        return False

    # Verifica se o nome de usuário contém apenas letras, números e underscore (_)
    if not re.match("^[a-zA-Z0-9_]*$", username):
        return False

    # Verifica se o username começa com uma letra
    if not username[0].isalpha():
        return False

    return True

def valid_email(email):
    # Verifica se o campo não está vazio
    if not email:
        return False
    
    # Verifica o formato do e-mail usando uma expressão regular
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return True
    
    return False

def validate_user_data(user):
    if not valid_username(user.username):
        raise HTTPException(status_code=200, detail="Invalid username")

    if not valid_email(user.email):
        raise HTTPException(status_code=200, detail="Invalid email")

    if not valid_password(user.password):
        raise HTTPException(status_code=200, detail="Invalid password")
    
    # muda todos os caractéres do username para minusculo
    user.username = user.username.lower()

def send_activation_email(email: str, activation_token: str):
    # Configurações do servidor SMTP
    SMTP_HOST = config("HOST_SMTP_UMBLER")
    SMTP_PORT = config("PORT_UMBLER", cast=int)
    SMTP_USERNAME = config("EMAIL_UMBLER")
    SMTP_PASSWORD = config("SENHA_UMBLER")

    # Crie a mensagem de email
    message = MIMEText(f"Clique no link para ativar sua conta: {activation_token}")
    message["Subject"] = "Ativação de conta"
    message["From"] = SMTP_USERNAME
    message["To"] = email

    # Envie o email
    with SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(message)

