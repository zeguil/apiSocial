from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
import bcrypt
from pydantic import BaseModel
from typing import Optional
import secrets
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = FastAPI()

# Definir modelos de dados e classes de tabela SQLAlchemy aqui

# ...

# Classe para representar a solicitação de redefinição de senha
class ResetPasswordRequest(BaseModel):
    email: str

# Classe para representar a alteração da senha
class ChangePasswordRequest(BaseModel):
    code: str
    new_password: str

# Rota para solicitar a redefinição de senha
@app.post("/reset-password")
def reset_password(reset_request: ResetPasswordRequest, session: Session = Depends(get_db)):
    # Verificar se o e-mail fornecido existe no banco de dados
    user = session.query(User).filter(User.email == reset_request.email).first()
    if not user:
        return {"message": "E-mail não encontrado"}

    # Gerar um código de redefinição de senha aleatório
    reset_code = secrets.token_hex(16)

    # Salvar o código no banco de dados
    user.reset_code = reset_code
    session.commit()

    # Enviar e-mail com o código de redefinição de senha para o usuário
    send_reset_email(user.email, reset_code)

    return {"message": "E-mail de redefinição de senha enviado"}

# Rota para alterar a senha usando o código de redefinição
@app.post("/change-password")
def change_password(change_request: ChangePasswordRequest, session: Session = Depends(get_db)):
    # Verificar se o código de redefinição e a nova senha correspondem a um usuário válido
    user = session.query(User).filter(User.reset_code == change_request.code).first()
    if not user:
        return {"message": "Código inválido"}

    # Atualizar a senha do usuário com a nova senha fornecida
    hashed_password = bcrypt.hashpw(change_request.new_password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password.decode('utf-8')
    user.reset_code = None
    session.commit()

    return {"message": "Senha alterada com sucesso"}

# Função para enviar o e-mail de redefinição de senha
def send_reset_email(email: str, code: str):
    message = Mail(
        from_email="your-email@example.com",
        to_emails=email,
        subject="Redefinição de senha",
        plain_text_content=f"Seu código de redefinição de senha é: {code}"
    )
    try:
        sg = SendGridAPIClient("YOUR_SENDGRID_API_KEY")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

# Restante do código do FastAPI e definição das rotas

# ...

