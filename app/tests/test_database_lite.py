from sqlalchemy import create_engine
from decouple import config

def test_database_connection():
    url = config('URLDB')
    engine = create_engine(url)
    
    try:
        connection = engine.connect()
        print("Conexão bem-sucedida!")
        connection.close()
    except Exception as e:
        assert False, f"Erro ao conectar: {e}"
