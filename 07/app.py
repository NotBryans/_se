from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory store for tasks
TASKS = []

# --- Core Server Business Logic (Tested in Unit Tests) ---
def calculate_discount(price: float, discount_percent: float) -> float:
    if price < 0 or not (0 <= discount_percent <= 100):
        raise ValueError("Invalid price or discount percentage")
    return round(price * (1 - discount_percent / 100.0), 2)

def validate_task_title(title: str) -> bool:
    if not isinstance(title, str):
        return False
    cleaned = title.strip()
    return 1 <= len(cleaned) <= 100

# --- Frontend HTML ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Week 7 Task & Discount App</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 640px; margin: 40px auto; padding: 0 20px; }
        .card { border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
        input, button { padding: 8px 12px; font-size: 14px; }
        button { cursor: pointer; background: #2563eb; color: white; border: none; border-radius: 4px; }
    </style>
</head>
<body>
    <h1 id="app-title">Task Manager</h1>
    <div class="card">
        <input id="task-input" type="text" placeholder="Enter new task..." />
        <button id="add-btn" onclick="addTask()">Add Task</button>
        <ul id="task-list"></ul>
    </div>

    <script>
        async function loadTasks() {
            const res = await fetch('/api/tasks');
            const data = await res.json();
            const list = document.getElementById('task-list');
            list.innerHTML = '';
            data.tasks.forEach(t => {
                const li = document.createElement('li');
                li.className = 'task-item';
                li.textContent = t.title;
                list.appendChild(li);
            });
        }

        async function addTask() {
            const input = document.getElementById('task-input');
            const title = input.value;
            const res = await fetch('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title })
            });
            if (res.ok) {
                input.value = '';
                await loadTasks();
            }
        }

        loadTasks();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

# --- Web API Endpoints (Tested in System / API Tests) ---
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": TASKS}), 200

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "")
    if not validate_task_title(title):
        return jsonify({"error": "Invalid task title"}), 400
    task = {"id": len(TASKS) + 1, "title": title.strip()}
    TASKS.append(task)
    return jsonify(task), 201

@app.route("/api/discount", methods=["POST"])
def api_discount():
    data = request.get_json(silent=True) or {}
    try:
        final_price = calculate_discount(
            float(data.get("price", 0)),
            float(data.get("discount", 0))
        )
        return jsonify({"final_price": final_price}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)