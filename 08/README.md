# Week 8 Project (Exercise 3 Implementation): CutTrack Pro

**CutTrack Pro** is a lightweight, self-hosted web application built to solve a real-world daily problem: tracking strict calorie deficits, macronutrient ratios (protein, carbs, fats), daily step counts, bodyweight trends, and High-Intensity Training (HIT) top sets in a single distraction-free interface without subscription paywalls.

## Key Features & Value Proposition
- **One-Click Staple Presets**: Log frequent whole-food staples (chicken breast, white rice, eggs, potatoes) in one click or enter custom meals.
- **Real-Time Macro & Deficit Progress**: Automatically aggregates daily calories, protein, carbs, and fats against daily cutting targets.
- **HIT Progressive Overload Logger**: Tracks working sets taken to muscular failure (`Weight × Reps @ RPE`).
- **Daily NEAT & Scale Tracking**: Records daily step counts and morning bodyweight by calendar date.
- **Persistent SQLite Storage**: Zero external database setup required—all logs persist locally in `cuttrack.db`.

## Tech Stack
- **Backend**: Python 3, Flask REST API
- **Database**: SQLite3 (`meals`, `workouts`, and `daily_metrics` relational tables)
- **Frontend**: Responsive Dark-Mode HTML5, CSS Grid, Vanilla Fetch JS
- **Testing**: `pytest` automated API & database integration tests

## How to Run Locally

```bash
pip install flask pytest
python app.py