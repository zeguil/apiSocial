from fastapi.testclient import TestClient

from main import app
from models.user import User

client = TestClient(app)

def test_create_user_sqlite():
    # Define os dados do usuário para teste
    user_data = {
        "username": "test_user",
        "password": "test_password"
    }

    # Envia a requisição POST para criar o usuário no banco de testes SQLite
    response = client.post("/user", json=user_data)

    # Verifica se a resposta está correta
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "username": "test_user"
    }

def test_create_user_postgres():
    # Define os dados do usuário para teste
    user_data = {
        "username": "test_user",
        "password": "test_password"
    }

    # Envia a requisição POST para criar o usuário no banco de dados PostgreSQL
    response = client.post("/user", json=user_data)

    # Verifica se a resposta está correta
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "username": "test_user"
    }
