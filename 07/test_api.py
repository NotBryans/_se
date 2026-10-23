import pytest
from app import app, TASKS

@pytest.fixture
def client():
    app.config["TESTING"] = True
    TASKS.clear()
    with app.test_client() as client:
        yield client

def test_get_empty_tasks(client):
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert res.get_json() == {"tasks": []}

def test_create_and_fetch_task(client):
    post_res = client.post("/api/tasks", json={"title": "Write API tests"})
    assert post_res.status_code == 201
    assert post_res.get_json()["title"] == "Write API tests"

    get_res = client.get("/api/tasks")
    assert len(get_res.get_json()["tasks"]) == 1

def test_create_invalid_task_returns_400(client):
    res = client.post("/api/tasks", json={"title": "   "})
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_discount_api_endpoint(client):
    res = client.post("/api/discount", json={"price": 200, "discount": 25})
    assert res.status_code == 200
    assert res.get_json()["final_price"] == 150.0