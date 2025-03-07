# backend/tests/test_categories.py
from fastapi.testclient import TestClient
from app.models import CategoryType

def test_get_all_categories(client, sample_categories):
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Alimentación"

def test_get_expense_categories(client, sample_categories):
    response = client.get("/categories/expenses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(cat["type"] == CategoryType.EXPENSE for cat in data)

def test_get_income_categories(client, sample_categories):
    response = client.get("/categories/incomes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == CategoryType.INCOME

def test_filter_categories_by_type(client, sample_categories):
    response = client.get("/categories/?type=expense")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(cat["type"] == CategoryType.EXPENSE for cat in data)