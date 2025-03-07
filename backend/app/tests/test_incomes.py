from fastapi.testclient import TestClient
from datetime import datetime

def test_create_income(client, authentication_token):
    current_date = datetime.now()
    income_data = {
        "amount": 1000.0,
        "source": "Test income",
        "date": current_date.isoformat(),  # Convertir a string ISO format
        "category_id": 3,
        "wallet_id": 1
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    response = client.post("/incomes/", json=income_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == income_data["amount"]
    assert data["source"] == income_data["source"]

def test_get_user_incomes(client, authentication_token):
    headers = {"Authorization": f"Bearer {authentication_token}"}
    response = client.get("/incomes/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)