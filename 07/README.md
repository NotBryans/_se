# Week 7 Assignment: Web Application with Three Levels of Testing

This project implements a full-stack Task & Discount Web Application in Python (Flask) and demonstrates three distinct testing methodologies:
1. **Unit Testing** (`test_unit.py`)
2. **System / Web API Testing** (`test_api.py`)[cite: 9]
3. **End-to-End (E2E) Headless Browser Testing** (`test_e2e.py` using Playwright)[cite: 9]

---

## 1. Overview of the Three Testing Levels

| Test Type | File | Target | Description |
| :--- | :--- | :--- | :--- |
| **1. Unit Test**[cite: 9] | `test_unit.py` | Server Functions | Directly tests server-side functions (`calculate_discount` and `validate_task_title`) for standard cases, edge boundaries, and invalid input exceptions. |
| **2. System / Web API Test**[cite: 9] | `test_api.py` | REST API Endpoints | Tests HTTP `GET /api/tasks`, `POST /api/tasks`, and `POST /api/discount` status codes (`200`, `201`, `400`) and JSON payloads. |
| **3. E2E Test**[cite: 9] | `test_e2e.py` | Full Web UI (Headless Browser)[cite: 9] | Launches a headless Chromium browser via **Playwright**[cite: 9], loads the live page, fills the input box, clicks the button, and verifies the DOM updates. |

---

## 2. Setup & How to Run the Tests

### Install Dependencies
```bash
pip install flask pytest playwright
playwright install chromium