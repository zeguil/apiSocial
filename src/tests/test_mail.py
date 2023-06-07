import os, sys, smtplib, logging as log
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from decouple import config
from fastapi import HTTPException
import re
import aiosmtplib
import asyncio

def validEmail(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True

def render_template(template, token, name):
    p = Path(__file__).parent.parent/'static'/'templates'
    templateLoader = FileSystemLoader(searchpath=Path(p))
    templateEnv = Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)

    data = {'token':token, 'name':name.title()}
    return templ.render(data)

def send_email(email, token, name):
    print('ENTROU NA FUNCÃO "SEND EMAIL"')
    html = render_template('emailActive.j2', token=token, name=name)

    # UMBLER VARS 
    HOST_SMTP_UMBLER = config('HOST_SMTP_UMBLER') 
    PORT_UMBLER = config('PORT_UMBLER') 
    EMAIL_UMBLER = config('EMAIL_UMBLER') 
    SENHA_UMBLER = config('SENHA_UMBLER') 
    
    #Entrando no servidor
    try:
        server = smtplib.SMTP(HOST_SMTP_UMBLER, PORT_UMBLER)
        server.starttls() # alguns casos
        server.login(EMAIL_UMBLER, SENHA_UMBLER)
        print('CONEXÃO SMTP ESTABELECIDA')
    except:
        raise HTTPException(status_code=500, detail="Erro ao estabelecer conexão SMTP")

    # Montando email
    message = MIMEMultipart()
    message['From'] = EMAIL_UMBLER
    message['To'] = email
    message['Subject'] = '[QuickLink] Ativação de Conta'
    message.attach(MIMEText(html, 'html'))

    try:
        # Enviar email
        log.info(f'sending email to {email}')
        server.sendmail(message['From'], message['To'], message.as_string())
        print(f"EMAIL ENVIADO PARA {email}")
    except Exception as e:
        log.error('Error sending email')
        log.exception(str(e))
    finally:
        # Fechar servidor
        server.quit()

send_email("zeguilhermelins@hotmail.com", "InplZ3VpbGhlcm1lbGluc0Bob3RtYWlsLmNvbSI.ZHdz_A.M1hNUzfrysA7obj7KtsszFfpCRs", "Henrique")

# vbleliss310700@gmail.com
# victoriabeatrizlelis@gmail.com
# barbara.oli12@hotmail.com