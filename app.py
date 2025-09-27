from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this for security (e.g., random string)

# Paths
DATA_DIR = 'data'
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.txt')
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize files
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        f.write("Tasks Log Started\n")

if not os.path.exists(USERS_FILE):
    # Sample users: email:password (add your own; in real app, hash passwords)
    sample_users = "user@example.com:pass123\nadmin@site.com:adminpass\n"
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        f.write(sample_users)
    print("Created sample users in data/users.txt. Add more as needed.")

def validate_user(email, password):
    """Simple check: Load users.txt and match email:password."""
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            stored = line.strip().split(':')
            if len(stored) == 2 and stored[0] == email and stored[1] == password:
                return True
    return False

@app.route('/')
def home():
    return render_template('first.html')  # Show selection page first

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        if validate_user(email, password):
            session['email'] = email
            return jsonify({'status': 'success', 'redirect': url_for('/tasks')})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid email or password. Try again.'})
    return render_template('login.html')

@app.route('/tasks')
def tasks_page():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'email' not in session:
        return jsonify({'status': 'error', 'message': 'Please login first'}), 401
    try:
        task = request.form.get('task', '').strip()
        priority = request.form.get('priority', 'Low')
        if not task:
            return jsonify({'status': 'error', 'message': 'Task cannot be empty'}), 400
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_email = session['email']
        entry = f"{timestamp} | User: {user_email} | {task} | Priority: {priority}\n"
        
        with open(TASKS_FILE, 'a', encoding='utf-8') as f:
            f.write(entry)
        
        print(f"Saved: {entry.strip()}")
        return jsonify({'status': 'success', 'message': 'Task saved!'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': f'Failed: {str(e)}'}), 500

@app.route('/view')
def view_tasks():
    if 'email' not in session:
        return redirect(url_for('login'))
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"<h1>Your Tasks (as {session['email']}):</h1><pre>{content}</pre><a href='/'>Back to Tasks</a> | <a href='/logout'>Logout</a>"
    return "No tasks yet. Add some!"

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("App starting. Login at http://127.0.0.1:5000/login")
    app.run(debug=True, port=5000)