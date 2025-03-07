from fastapi.testclient import TestClient
from datetime import datetime
import pytest
from app.models import CategoryType

def test_create_expense(client, authentication_token, sample_categories, test_user):
    expense_data = {
        "description": "Test expense",
        "amount": 100.0,
        "date": datetime.now().isoformat(),
        "category_id": 1,
        "expense_type": "único"
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    response = client.post("/expenses/", json=expense_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == expense_data["amount"]
    assert data["description"] == expense_data["description"]
    assert "id" in data

def test_get_user_expenses(client, authentication_token, test_user):
    # Primero creamos un gasto sin enviar "user_id"
    expense_data = {
        "description": "Test expense",
        "amount": 100.0,
        "date": datetime.now().isoformat(),
        "category_id": 1,
        "expense_type": "único"
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    client.post("/expenses/", json=expense_data, headers=headers)
    
    # Ahora obtenemos los gastos
    response = client.get("/expenses/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["description"] == expense_data["description"]

def test_create_expense_invalid_category(client, authentication_token, test_user):
    expense_data = {
        "description": "Test expense",
        "amount": 100.0,
        "date": datetime.now().isoformat(),
        "category_id": 1,  # Categoría que no existe
        "expense_type": "único"
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    response = client.post("/expenses/", json=expense_data, headers=headers)
    assert response.status_code == 404

def test_create_expense_without_auth(client):
    expense_data = {
        "description": "Test expense",
        "amount": 100.0,
        "date": datetime.now().isoformat(),
        "category_id": 1,
        "expense_type": "único"
    }
    response = client.post("/expenses/", json=expense_data)
    assert response.status_code == 401

def test_get_expenses_by_date_range(client, authentication_token):
    headers = {"Authorization": f"Bearer {authentication_token}"}
    start_date = datetime.now().date().isoformat()
    end_date = datetime.now().date().isoformat()
    
    response = client.get(
        f"/expenses/?start_date={start_date}&end_date={end_date}", 
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)