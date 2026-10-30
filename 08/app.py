import sqlite3
from datetime import date
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
DB_PATH = "cuttrack.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT NOT NULL,
            food_name TEXT NOT NULL,
            calories INTEGER NOT NULL,
            protein REAL NOT NULL,
            carbs REAL NOT NULL,
            fats REAL NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT NOT NULL,
            exercise TEXT NOT NULL,
            weight_kg REAL NOT NULL,
            reps INTEGER NOT NULL,
            rpe INTEGER NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_metrics (
            log_date TEXT PRIMARY KEY,
            steps INTEGER DEFAULT 0,
            bodyweight REAL DEFAULT 0.0,
            calorie_target INTEGER DEFAULT 2100,
            protein_target INTEGER DEFAULT 180
        )
    """)
    conn.commit()
    conn.close()


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CutTrack Pro — Nutrition & HIT Training Tracker</title>
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --border: #334155;
            --text: #f8fafc;
            --muted: #94a3b8;
            --accent: #3b82f6;
            --success: #10b981;
            --danger: #ef4444;
        }
        * { box-sizing: border-box; }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 28px 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 12px;
        }
        h1 { margin: 0; font-size: 24px; }
        .sub { color: var(--muted); font-size: 14px; margin-top: 4px; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .two-col {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 20px;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }
        .stat-label { font-size: 13px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }
        .stat-val { font-size: 26px; font-weight: 700; margin: 8px 0; }
        .bar-bg { background: #0b1120; height: 8px; border-radius: 999px; overflow: hidden; }
        .bar-fill { background: var(--accent); height: 100%; transition: width 0.25s ease; }
        .bar-fill.green { background: var(--success); }
        input, select, button {
            padding: 9px 12px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #0b1120;
            color: var(--text);
            font-size: 14px;
        }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
        .full { grid-column: 1 / -1; }
        button {
            background: var(--accent);
            border: none;
            font-weight: 600;
            cursor: pointer;
        }
        button:hover { opacity: 0.9; }
        .del-btn {
            background: transparent;
            color: var(--danger);
            padding: 4px 8px;
            font-size: 12px;
            border: 1px solid var(--danger);
        }
        .preset-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; }
        .preset {
            background: #334155;
            font-size: 12px;
            padding: 5px 10px;
        }
        ul { list-style: none; padding: 0; margin: 14px 0 0 0; }
        li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
        }
        .meta { color: var(--muted); font-size: 12px; }
    </style>
</head>
<body>
<div class="container">
    <header>
        <div>
            <h1>CutTrack Pro</h1>
            <div class="sub">Macro Deficit, Daily Steps & High-Intensity Training Dashboard</div>
        </div>
        <div>
            <input type="date" id="datePicker" />
        </div>
    </header>

    <div class="grid">
        <div class="card">
            <div class="stat-label">Calories Consumed</div>
            <div class="stat-val" id="calStat">0 / 2100 kcal</div>
            <div class="bar-bg"><div class="bar-fill" id="calBar" style="width:0%"></div></div>
        </div>
        <div class="card">
            <div class="stat-label">Protein Intake</div>
            <div class="stat-val" id="proStat">0 / 180 g</div>
            <div class="bar-bg"><div class="bar-fill green" id="proBar" style="width:0%"></div></div>
        </div>
        <div class="card">
            <div class="stat-label">Carbs / Fats</div>
            <div class="stat-val" id="cfStat">0g C / 0g F</div>
            <div class="meta">Balanced Energy Split</div>
        </div>
        <div class="card">
            <div class="stat-label">Steps & Bodyweight</div>
            <div class="stat-val" id="stepStat">0 steps</div>
            <div style="display:flex; gap:6px; margin-top:8px;">
                <input type="number" id="stepsInput" placeholder="Steps" style="width:50%">
                <input type="number" step="0.1" id="bwInput" placeholder="kg" style="width:50%">
                <button onclick="saveMetrics()">Save</button>
            </div>
        </div>
    </div>

    <div class="two-col">
        <div class="card">
            <h3 style="margin-top:0">Log Nutrition</h3>
            <div class="preset-row">
                <button class="preset" onclick="quickAdd('Chicken Breast (200g)', 330, 62, 0, 7)">+ Chicken 200g</button>
                <button class="preset" onclick="quickAdd('White Rice (200g)', 260, 5.4, 56, 0.6)">+ Rice 200g</button>
                <button class="preset" onclick="quickAdd('Whole Eggs (3)', 215, 18.9, 1.2, 14.5)">+ 3 Eggs</button>
                <button class="preset" onclick="quickAdd('Potato (250g)', 193, 5, 44, 0.3)">+ Potato 250g</button>
            </div>
            <div class="form-row">
                <input class="full" id="foodName" placeholder="Food item name" />
                <input type="number" id="foodCal" placeholder="Calories (kcal)" />
                <input type="number" step="0.1" id="foodPro" placeholder="Protein (g)" />
                <input type="number" step="0.1" id="foodCarb" placeholder="Carbs (g)" />
                <input type="number" step="0.1" id="foodFat" placeholder="Fats (g)" />
                <button class="full" onclick="addMeal()">Add Food Entry</button>
            </div>
            <ul id="mealList"></ul>
        </div>

        <div class="card">
            <h3 style="margin-top:0">Log HIT Working Set</h3>
            <div class="form-row">
                <input class="full" id="exName" placeholder="Exercise (e.g., Incline Press, Weighted Pull-up)" />
                <input type="number" step="0.5" id="exWeight" placeholder="Weight (kg)" />
                <input type="number" id="exReps" placeholder="Reps to Failure" />
                <select id="exRpe" class="full">
                    <option value="10">RPE 10 — Absolute Muscular Failure</option>
                    <option value="9">RPE 9 — 1 Rep in Reserve</option>
                    <option value="8">RPE 8 — 2 Reps in Reserve</option>
                </select>
                <button class="full" onclick="addWorkout()">Log Top Set</button>
            </div>
            <ul id="workoutList"></ul>
        </div>
    </div>
</div>

<script>
    const picker = document.getElementById('datePicker');
    picker.value = new Date().toISOString().split('T')[0];
    picker.addEventListener('change', loadDay);

    async function loadDay() {
        const d = picker.value;
        const res = await fetch(`/api/day?date=${d}`);
        const data = await res.json();

        const cals = data.totals.calories;
        const pro = data.totals.protein;
        const calTarget = data.metrics.calorie_target;
        const proTarget = data.metrics.protein_target;

        document.getElementById('calStat').textContent = `${cals} / ${calTarget} kcal`;
        document.getElementById('calBar').style.width = `${Math.min(100, (cals / calTarget) * 100)}%`;

        document.getElementById('proStat').textContent = `${pro.toFixed(1)} / ${proTarget} g`;
        document.getElementById('proBar').style.width = `${Math.min(100, (pro / proTarget) * 100)}%`;

        document.getElementById('cfStat').textContent = `${data.totals.carbs.toFixed(1)}g C / ${data.totals.fats.toFixed(1)}g F`;
        document.getElementById('stepStat').textContent = `${data.metrics.steps.toLocaleString()} steps (${data.metrics.bodyweight || '--'} kg)`;
        document.getElementById('stepsInput').value = data.metrics.steps || '';
        document.getElementById('bwInput').value = data.metrics.bodyweight || '';

        const mealList = document.getElementById('mealList');
        mealList.innerHTML = '';
        data.meals.forEach(m => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div>
                    <strong>${m.food_name}</strong>
                    <div class="meta">${m.calories} kcal • ${m.protein}g P • ${m.carbs}g C • ${m.fats}g F</div>
                </div>
                <button class="del-btn" onclick="deleteMeal(${m.id})">Delete</button>
            `;
            mealList.appendChild(li);
        });

        const workoutList = document.getElementById('workoutList');
        workoutList.innerHTML = '';
        data.workouts.forEach(w => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div>
                    <strong>${w.exercise}</strong>
                    <div class="meta">${w.weight_kg} kg × ${w.reps} reps @ RPE ${w.rpe}</div>
                </div>
                <button class="del-btn" onclick="deleteWorkout(${w.id})">Delete</button>
            `;
            workoutList.appendChild(li);
        });
    }

    async function addMeal() {
        const payload = {
            log_date: picker.value,
            food_name: document.getElementById('foodName').value,
            calories: Number(document.getElementById('foodCal').value),
            protein: Number(document.getElementById('foodPro').value || 0),
            carbs: Number(document.getElementById('foodCarb').value || 0),
            fats: Number(document.getElementById('foodFat').value || 0)
        };
        if (!payload.food_name || payload.calories <= 0) return;
        await fetch('/api/meals', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        ['foodName','foodCal','foodPro','foodCarb','foodFat'].forEach(id => document.getElementById(id).value = '');
        loadDay();
    }

    async function quickAdd(name, cal, pro, carb, fat) {
        await fetch('/api/meals', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                log_date: picker.value,
                food_name: name,
                calories: cal,
                protein: pro,
                carbs: carb,
                fats: fat
            })
        });
        loadDay();
    }

    async function deleteMeal(id) {
        await fetch(`/api/meals/${id}`, { method: 'DELETE' });
        loadDay();
    }

    async function addWorkout() {
        const payload = {
            log_date: picker.value,
            exercise: document.getElementById('exName').value,
            weight_kg: Number(document.getElementById('exWeight').value),
            reps: Number(document.getElementById('exReps').value),
            rpe: Number(document.getElementById('exRpe').value)
        };
        if (!payload.exercise || payload.reps <= 0) return;
        await fetch('/api/workouts', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        ['exName','exWeight','exReps'].forEach(id => document.getElementById(id).value = '');
        loadDay();
    }

    async function deleteWorkout(id) {
        await fetch(`/api/workouts/${id}`, { method: 'DELETE' });
        loadDay();
    }

    async function saveMetrics() {
        await fetch('/api/metrics', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                log_date: picker.value,
                steps: Number(document.getElementById('stepsInput').value || 0),
                bodyweight: Number(document.getElementById('bwInput').value || 0)
            })
        });
        loadDay();
    }

    loadDay();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/day", methods=["GET"])
def get_day_summary():
    log_date = request.args.get("date", str(date.today()))
    conn = get_db()
    cur = conn.cursor()

    meals = [dict(r) for r in cur.execute("SELECT * FROM meals WHERE log_date = ? ORDER BY id DESC", (log_date,)).fetchall()]
    workouts = [dict(r) for r in cur.execute("SELECT * FROM workouts WHERE log_date = ? ORDER BY id DESC", (log_date,)).fetchall()]
    row = cur.execute("SELECT * FROM daily_metrics WHERE log_date = ?", (log_date,)).fetchone()
    conn.close()

    metrics = dict(row) if row else {
        "log_date": log_date,
        "steps": 0,
        "bodyweight": 0.0,
        "calorie_target": 2100,
        "protein_target": 180
    }

    totals = {
        "calories": sum(m["calories"] for m in meals),
        "protein": round(sum(m["protein"] for m in meals), 1),
        "carbs": round(sum(m["carbs"] for m in meals), 1),
        "fats": round(sum(m["fats"] for m in meals), 1),
    }

    return jsonify({"date": log_date, "meals": meals, "workouts": workouts, "metrics": metrics, "totals": totals})


@app.route("/api/meals", methods=["POST"])
def add_meal():
    data = request.get_json(force=True)
    if not data.get("food_name") or int(data.get("calories", 0)) <= 0:
        return jsonify({"error": "Invalid meal input"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO meals (log_date, food_name, calories, protein, carbs, fats) VALUES (?, ?, ?, ?, ?, ?)",
        (
            data.get("log_date", str(date.today())),
            data["food_name"].strip(),
            int(data["calories"]),
            float(data.get("protein", 0)),
            float(data.get("carbs", 0)),
            float(data.get("fats", 0)),
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, "status": "created"}), 201


@app.route("/api/meals/<int:meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    conn = get_db()
    conn.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"}), 200


@app.route("/api/workouts", methods=["POST"])
def add_workout():
    data = request.get_json(force=True)
    if not data.get("exercise") or int(data.get("reps", 0)) <= 0:
        return jsonify({"error": "Invalid workout input"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO workouts (log_date, exercise, weight_kg, reps, rpe) VALUES (?, ?, ?, ?, ?)",
        (
            data.get("log_date", str(date.today())),
            data["exercise"].strip(),
            float(data.get("weight_kg", 0)),
            int(data["reps"]),
            int(data.get("rpe", 10)),
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id, "status": "created"}), 201


@app.route("/api/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    conn = get_db()
    conn.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"}), 200


@app.route("/api/metrics", methods=["POST"])
def update_metrics():
    data = request.get_json(force=True)
    log_date = data.get("log_date", str(date.today()))
    steps = int(data.get("steps", 0))
    bodyweight = float(data.get("bodyweight", 0.0))

    conn = get_db()
    conn.execute("""
        INSERT INTO daily_metrics (log_date, steps, bodyweight)
        VALUES (?, ?, ?)
        ON CONFLICT(log_date) DO UPDATE SET
            steps = excluded.steps,
            bodyweight = excluded.bodyweight
    """, (log_date, steps, bodyweight))
    conn.commit()
    conn.close()
    return jsonify({"status": "updated"}), 200


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)