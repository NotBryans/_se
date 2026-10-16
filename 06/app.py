import os
import socket
import psycopg2
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "mydb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASS", "postgres")
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Docker Microservices Dashboard</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 20px; background: #f8fafc; color: #1e293b; }
        .card { background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 20px; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: bold; background: #e0f2fe; color: #0369a1; margin-right: 8px; }
        input[type="text"] { padding: 8px 12px; width: 70%; border: 1px solid #cbd5e1; border-radius: 6px; }
        button { padding: 8px 16px; background: #2563eb; color: white; border: none; border-radius: 6px; cursor: pointer; }
        ul { padding-left: 20px; }
        li { margin-bottom: 8px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🐳 Docker Microservices System</h2>
        <p>
            <span class="badge">Nginx (Reverse Proxy)</span>
            <span class="badge">Python Flask ({{ hostname }})</span>
            <span class="badge">PostgreSQL 15</span>
        </p>
        <p><strong>Database Status:</strong> {{ db_status }}</p>
    </div>

    <div class="card">
        <h3>Add Message to PostgreSQL</h3>
        <form method="POST" action="/add">
            <input type="text" name="message" placeholder="Enter a test message..." required>
            <button type="submit">Save to DB</button>
        </form>
        <h4>Database Records (Total: {{ records|length }}):</h4>
        <ul>
            {% for r in records %}
                <li><strong>#{{ r[0] }}</strong>: {{ r[1] }} <small style="color:#64748b;">({{ r[2] }})</small></li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    records = []
    db_status = "Connected"
    try:
        init_db()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, message, created_at FROM visits ORDER BY id DESC LIMIT 10;")
        records = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        db_status = f"Connection Failed: {e}"

    return render_template_string(
        HTML_TEMPLATE,
        hostname=socket.gethostname(),
        db_status=db_status,
        records=records
    )

@app.route("/add", methods=["POST"])
def add_message():
    msg = request.form.get("message")
    if msg:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO visits (message) VALUES (%s);", (msg,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)