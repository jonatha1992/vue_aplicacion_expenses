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

def test_delete_expense(client, authentication_token, test_user):
    # First create an expense to delete
    expense_data = {
        "description": "Expense to delete",
        "amount": 100.0,
        "date": datetime.now().isoformat(),
        "category_id": 1,
        "expense_type": "único"
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    
    # Create the expense
    create_response = client.post("/expenses/", json=expense_data, headers=headers)
    assert create_response.status_code == 200
    created_expense = create_response.json()
    
    # Delete the expense
    delete_response = client.delete(f"/expenses/{created_expense['id']}/", headers=headers)
    assert delete_response.status_code == 200
    
    # Verify expense was deleted by checking the expenses list
    list_response = client.get("/expenses/", headers=headers)
    assert list_response.status_code == 200
    expenses = list_response.json()
    assert all(expense["id"] != created_expense["id"] for expense in expenses)


def test_update_expense(client, authentication_token, test_user):
    # First create an expense to update
    expense_data = {
        "description": "Original expense",
        "amount": 100.0,
        "date": datetime.now().isoformat(),
        "category_id": 1,
        "expense_type": "único"
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    
    # Create the expense
    create_response = client.post("/expenses/", json=expense_data, headers=headers)
    assert create_response.status_code == 200
    created_expense = create_response.json()
    
    # Update data
    update_data = {
        "description": "Updated expense",
        "amount": 150.0,
        "date": datetime.now().isoformat(),
        "category_id": 1,
        "expense_type": "único"
    }
    
    # Update the expense
    update_response = client.put(f"/expenses/{created_expense['id']}/", json=update_data, headers=headers)
    assert update_response.status_code == 200
    updated_expense = update_response.json()
    
    # Verify the expense was updated correctly
    assert updated_expense["description"] == update_data["description"]
    assert updated_expense["amount"] == update_data["amount"]
    assert updated_expense["id"] == created_expense["id"]

def test_delete_expense_unauthorized(client):
    # Try to delete without authentication
    response = client.delete("/expenses/1/")
    assert response.status_code == 401




