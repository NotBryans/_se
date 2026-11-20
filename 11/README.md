# 期末專題 (Final Project): CutTrack Pro — Full-Stack Nutrition & HIT Training Tracker

## 1. 專題簡介 (Project Overview)
**CutTrack Pro** is a self-hosted, full-stack web application designed to track daily calorie deficits, macronutrient intake (protein, carbs, fats), daily step counts (NEAT), morning bodyweight trends, and High-Intensity Training (HIT) progressive overload sets in one distraction-free dashboard.

Most commercial fitness apps lock basic macro tracking or workout logging behind monthly subscriptions. CutTrack Pro solves this by providing a fast, local-first web platform with persistent SQLite storage, one-click staple food presets, and automated test coverage.

---

## 2. 核心功能 (Core Features)
- **Daily Calorie & Macro Dashboard**: Real-time aggregation of calories, protein, carbs, and fats with visual progress bars against customizable daily cutting targets.
- **One-Click Staple Food Presets**: Instant logging for frequently eaten whole foods (chicken breast, white rice, whole eggs, potatoes) alongside custom meal entry and deletion.
- **HIT Progressive Overload Logger**: Tracks top working sets (`Exercise`, `Weight (kg)`, `Reps`, and `RPE 8–10`) to monitor strength retention during a cut.
- **Daily Metrics & Date Navigation**: Logs daily step counts and bodyweight per calendar date, allowing users to review past days effortlessly.
- **RESTful API & Automated Testing**: Full CRUD endpoints backed by `pytest` integration tests and headless E2E verification.

---

## 3. 系統架構與技術棧 (System Architecture & Tech Stack)
- **Frontend**: HTML5, CSS Grid (Dark Mode UI), Vanilla JavaScript (`Fetch API`)
- **Backend**: Python 3, Flask REST API
- **Database**: SQLite3 (`meals`, `workouts`, and `daily_metrics` tables)
- **Testing**: `pytest` (Unit & API integration tests)
- **Deployment / Containerization**: Docker & `docker-compose` ready

```text
[ Browser (HTML/CSS/JS) ]
           │  HTTP / JSON (Fetch API)
           ▼
[ Flask REST API Server (app.py) ]
           │  SQL Queries
           ▼
[ SQLite3 Database (cuttrack.db) ]
git add 11/
git commit -m "Add Week 11 Final Project README.md"
git push
cd "C:\Users\bryan\OneDrive\Documents\Bryan VS Code\_se"
mkdir -Force 11 | Out-Null

@'
# 期末專題 (Final Project): CutTrack Pro — Full-Stack Nutrition & HIT Training Tracker

## 1. 專題簡介 (Project Overview)
**CutTrack Pro** is a self-hosted, full-stack web application designed to track daily calorie deficits, macronutrient intake (protein, carbs, fats), daily step counts (NEAT), morning bodyweight trends, and High-Intensity Training (HIT) progressive overload sets in one distraction-free dashboard.

## 2. 核心功能 (Core Features)
- **Daily Calorie & Macro Dashboard**: Real-time aggregation of calories, protein, carbs, and fats with visual progress bars against daily cutting targets.
- **One-Click Staple Food Presets**: Instant logging for frequently eaten whole foods (chicken breast, white rice, whole eggs, potatoes) alongside custom meal entry and deletion.
- **HIT Progressive Overload Logger**: Tracks top working sets (Exercise, Weight, Reps, and RPE 8-10) to monitor strength retention during a cut.
- **Daily Metrics & Date Navigation**: Logs daily step counts and bodyweight per calendar date.
- **RESTful API & Automated Testing**: Full CRUD endpoints backed by pytest integration tests.

## 3. 系統架構與技術棧 (System Architecture & Tech Stack)
- **Frontend**: HTML5, CSS Grid (Dark Mode UI), Vanilla JavaScript (Fetch API)
- **Backend**: Python 3, Flask REST API
- **Database**: SQLite3 (meals, workouts, and daily_metrics tables)
- **Testing**: pytest (Unit & API integration tests)
- **Architecture Flow**: Browser (HTML/CSS/JS) -> Flask REST API Server (app.py) -> SQLite3 Database (cuttrack.db)

## 4. API 端點設計 (API Endpoints)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | /api/day?date=YYYY-MM-DD | Fetch all meals, workouts, metrics, and macro totals for a date |
| POST | /api/meals | Add a new food entry |
| DELETE | /api/meals/<id> | Delete a food entry |
| POST | /api/workouts | Log a new HIT working set |
| DELETE | /api/workouts/<id> | Delete a workout entry |
| POST | /api/metrics | Update daily steps and bodyweight |

## 5. 安裝與執行方式 (Setup & Usage)
1. Install dependencies: `pip install flask pytest`
2. Run the web application: `python ../08/app.py`
3. Run automated tests: `pytest ../08/test_app.py -v`
4. Open `http://127.0.0.1:5000` in your browser.

## 6. 期末開發進度與規劃 (Roadmap)
- [x] Phase 1: Core Flask backend, SQLite schema, and Dark Mode dashboard (08/app.py)
- [x] Phase 2: Automated API & database test suite (08/test_app.py)
- [ ] Phase 3: Weekly calorie/bodyweight trend charts and CSV export
- [ ] Phase 4: Final polish, Docker packaging, and live demo

## 7. AI 協作說明 (AI Collaboration)
Developed with assistance from Google Gemini for system architecture, UI design, and automated testing.
