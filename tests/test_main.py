from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_and_read_item():
    # Create item
    payload = {"title": "CI Test Task", "description": "Verify DB insert", "completed": False}
    post_res = client.post("/api/v1/items/", json=payload)
    assert post_res.status_code == 201
    data = post_res.json()
    assert data["title"] == payload["title"]
    item_id = data["id"]

    # Read item
    get_res = client.get(f"/api/v1/items/{item_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == payload["title"]