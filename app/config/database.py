from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

url = config('URLDB')

engine = create_engine(url)

try:
    connection = engine.connect()
    print("Conexão bem-sucedida!")
    connection.close()
except Exception as e:
    print("Erro ao conectar:", e)