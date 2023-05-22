from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

def test_database_connection():
    url = "postgresql://postgres:123@localhost:5432/apidb"
    engine = create_engine(url)
    try:
        connection = engine.connect()
        print("Conexão bem-sucedida!")
        connection.close()
    except Exception as e:
        assert False, f"Erro ao conectar: {e}"

test_database_connection()
