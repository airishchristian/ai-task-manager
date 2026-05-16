# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
from app.main import app
from app.dependencies.database import get_db

# ✅ Define the test database URL
TEST_DATABASE_URL = "sqlite://"

# ✅ Create a test engine with proper connect_args
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(name="session")
def session_fixture():
    # Create all tables before each test
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session
    # Drop all tables after each test for a clean slate
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Override get_db to use our test session
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    # Clear overrides after test
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
        },
    )
    return response.json()


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(client: TestClient, test_user):
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",   # ✅ matches UserLogin schema
            "password": "testpass123",
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
