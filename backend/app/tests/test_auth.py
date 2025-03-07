from fastapi.testclient import TestClient

def test_register_user(client):
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "test123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert "id" in data
    
def test_login_user(client, test_user):
    login_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data