import os
import pytest

# 1. Ensure DATABASE_URL is set before importing app modules
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# 2. Setup an isolated, in-memory SQLite engine that persists across threads
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Fixture to create fresh tables per test session and clean up after
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# 4. Override the app's get_db dependency to use the test session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- Test Cases ---

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"

def test_create_and_read_item():
    # Create item
    payload = {
        "title": "CI Test Task",
        "description": "Verify DB insert",
        "completed": False
    }
    post_res = client.post("/api/v1/items/", json=payload)
    assert post_res.status_code in [200, 201]
    data = post_res.json()
    assert data["title"] == payload["title"]
    item_id = data["id"]

    # Read items
    get_res = client.get(f"/api/v1/items/{item_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == payload["title"]