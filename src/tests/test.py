
import time
import re

nome = "1ose123232"

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

if not valid_password(nome):
    print("senha invalida")

else:
    print('passou')