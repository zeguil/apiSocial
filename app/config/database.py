from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = 'postgresql://postgres:123@localhost:5432/apidb'

engine = create_engine(url)

try:
    connection = engine.connect()
    print("Conexão bem-sucedida!")
    connection.close()
except Exception as e:
    print("Erro ao conectar:", e)