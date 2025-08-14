from flask import Flask, request, render_template
import sqlite3
from datetime import datetime
import user_agents
import os
DB_PATH = os.path.join(os.path.dirname(__file__), 'honeypot.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT,
                    browser TEXT,
                    os TEXT,
                    path TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)

# Setup Database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT,
                    browser TEXT,
                    os TEXT,
                    path TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# Fake Login Page (Honeypot)
@app.route('/')
def fake_login():
    return render_template('honeypot.html')

# Log All Requests
@app.before_request
def log_request():
    ua_string = request.headers.get('User-Agent')
    user_agent = user_agents.parse(ua_string)
    ip = request.remote_addr
    browser = user_agent.browser.family
    os = user_agent.os.family
    path = request.path
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()
    c.execute("INSERT INTO logs (ip, browser, os, path, timestamp) VALUES (?, ?, ?, ?, ?)",
              (ip, browser, os, path, timestamp))
    conn.commit()
    conn.close()

# Admin View
@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
