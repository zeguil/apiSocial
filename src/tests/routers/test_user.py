from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_list_users():
    
    response = client.get('/user')

    assert response.status_code == 200

def test_create_users():
    new_count = {
        "id" : 9,
        "user": "Carlos",
        "age" : 23
    }

    response = client.post('/user', json=new_count)

    assert response.status_code == 201
