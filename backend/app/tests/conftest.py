import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import CategoryDB, CategoryType, UserDB
from app.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    user = UserDB(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("test123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def sample_categories(db_session):
    categories = [
        CategoryDB(name="Alimentación", type=CategoryType.EXPENSE),
        CategoryDB(name="Transporte", type=CategoryType.EXPENSE),
        CategoryDB(name="Salario", type=CategoryType.INCOME)
    ]
    for category in categories:
        db_session.add(category)
    db_session.commit()
    return categories

# @pytest.fixture
# def authentication_token(client, test_user):
#     login_data = {
#         "username": "testuser",
#         "password": "test123"
#     }
#     response = client.post("/auth/login", json=login_data)
#     assert response.status_code == 200
#     data = response.json()
#     return data["access_token"]


@pytest.fixture
def authentication_token(client, test_user):
    login_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    return data["access_token"]