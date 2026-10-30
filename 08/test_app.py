import os
import tempfile
import pytest
import app as cuttrack


@pytest.fixture
def client():
    fd, temp_path = tempfile.mkstemp()
    os.close(fd)
    cuttrack.DB_PATH = temp_path
    cuttrack.init_db()
    cuttrack.app.config["TESTING"] = True
    with cuttrack.app.test_client() as client:
        yield client
    os.remove(temp_path)


def test_log_and_aggregate_meals(client):
    client.post("/api/meals", json={
        "log_date": "2026-10-30",
        "food_name": "Chicken Breast 200g",
        "calories": 330,
        "protein": 62,
        "carbs": 0,
        "fats": 7
    })
    client.post("/api/meals", json={
        "log_date": "2026-10-30",
        "food_name": "White Rice 200g",
        "calories": 260,
        "protein": 5.4,
        "carbs": 56,
        "fats": 0.6
    })

    res = client.get("/api/day?date=2026-10-30")
    data = res.get_json()
    assert res.status_code == 200
    assert data["totals"]["calories"] == 590
    assert data["totals"]["protein"] == 67.4


def test_workout_and_metrics_flow(client):
    w_res = client.post("/api/workouts", json={
        "log_date": "2026-10-30",
        "exercise": "Incline Dumbbell Press",
        "weight_kg": 35.0,
        "reps": 8,
        "rpe": 10
    })
    assert w_res.status_code == 201

    m_res = client.post("/api/metrics", json={
        "log_date": "2026-10-30",
        "steps": 15000,
        "bodyweight": 74.5
    })
    assert m_res.status_code == 200

    summary = client.get("/api/day?date=2026-10-30").get_json()
    assert len(summary["workouts"]) == 1
    assert summary["metrics"]["steps"] == 15000
    assert summary["metrics"]["bodyweight"] == 74.5