import pytest
from sqlalchemy import create_engine

@pytest.mark.test
def test_database_connection():
    url = 'postgresql://postgres:123@localhost:5432/apidb'
    engine = create_engine(url)

    try:
        connection = engine.connect()
        assert connection is not None
        connection.close()
    except Exception as e:
        pytest.fail(f"Falha ao conectar ao banco de dados: {e}")
