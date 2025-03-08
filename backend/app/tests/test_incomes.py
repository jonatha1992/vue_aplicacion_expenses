from fastapi.testclient import TestClient
from datetime import datetime, timezone

def test_create_income(client, authentication_token):
    current_date = datetime.now(timezone.utc)
    income_data = {
        "amount": 1000.0,
        "source": "Test income",
        "date": current_date.isoformat(),  # Use UTC datetime object
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
    # Primero creamos un ingreso para asegurarnos que hay datos
    current_date = datetime.now(timezone.utc)
    income_data = {
        "amount": 1000.0,
        "source": "Test income",
        "date": current_date.isoformat(),  # Use UTC datetime object
        "category_id": 3,
        "wallet_id": 1
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    client.post("/incomes/", json=income_data, headers=headers)
    
    # Ahora obtenemos los ingresos
    response = client.get("/incomes/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["amount"] == income_data["amount"]



def test_delete_income(client, authentication_token):
    # Primero creamos un ingreso para 
    current_date = datetime.now(timezone.utc)
    income_data = {
        "amount": 1000.0,
        "source": "Income to delete",
        "date": current_date.isoformat(),  # Use UTC datetime object
        "category_id": 3,
        "wallet_id": 1
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    
    # Crear el ingreso
    create_response = client.post("/incomes/", json=income_data, headers=headers)
    assert create_response.status_code == 200
    created_income = create_response.json()
    
    # Eliminar el ingreso
    delete_response = client.delete(f"/incomes/{created_income['id']}", headers=headers)
    assert delete_response.status_code == 200
    
    # Verificar que el ingreso fue eliminado
    get_response = client.get(f"/incomes/{created_income['id']}", headers=headers)
    assert get_response.status_code == 404




def test_update_income(client, authentication_token):
    # Primero creamos un ingreso
    current_date = datetime.now(timezone.utc)  # Use UTC datetime object
    income_data = {
        "amount": 1000.0,
        "source": "Original income",
        "date": current_date,
        "category_id": 3,
        "wallet_id": 1
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    
    # Crear el ingreso
    create_response = client.post("/incomes/", json=income_data, headers=headers)
    assert create_response.status_code == 200
    created_income = create_response.json()
    
    # Datos actualizados
    update_data = {
        "amount": 1500.0,
        "source": "Updated income",
        "date": current_date,  # Use same datetime object
        "category_id": 3,
        "wallet_id": 1
    }
    
    # Actualizar el ingreso
    update_response = client.put(f"/incomes/{created_income['id']}", json=update_data, headers=headers)
    assert update_response.status_code == 200
    updated_income = update_response.json()
    
    # Verificar la actualización
    assert updated_income["amount"] == update_data["amount"]
    assert updated_income["source"] == update_data["source"]
    assert updated_income["id"] == created_income["id"]
    
def test_get_income_by_id(client, authentication_token):
    # Crear un ingreso
    income_data = {
        "amount": 1000.0,
        "source": "Test income",
        "date": datetime.now(timezone.utc),  # Use UTC datetime object
        "category_id": 3,
        "wallet_id": 1
    }
    headers = {"Authorization": f"Bearer {authentication_token}"}
    
    # Crear el ingreso
    create_response = client.post("/incomes/", json=income_data, headers=headers)
    assert create_response.status_code == 200
    created_income = create_response.json()
    
    # Obtener el ingreso por ID
    response = client.get(f"/incomes/{created_income['id']}", headers=headers)
    assert response.status_code == 200
    income = response.json()
    assert income["id"] == created_income["id"]
    assert income["amount"] == income_data["amount"]
    assert income["source"] == income_data["source"]

def test_delete_nonexistent_income(client, authentication_token):
    headers = {"Authorization": f"Bearer {authentication_token}"}
    response = client.delete("/incomes/99999", headers=headers)
    assert response.status_code == 404

def test_update_nonexistent_income(client, authentication_token):
    headers = {"Authorization": f"Bearer {authentication_token}"}
    update_data = {
        "amount": 1500.0,
        "source": "Updated income",
        "date": datetime.now(timezone.utc),  # Use UTC datetime object
        "category_id": 3,
        "wallet_id": 1
    }
    response = client.put("/incomes/99999", json=update_data, headers=headers)
    assert response.status_code == 404