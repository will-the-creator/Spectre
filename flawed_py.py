from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

# Vulnerable endpoint: SQL Injection
@app.route('/user/<username>')
def get_user(username):
    conn = get_db_connection()
    # SQL Injection vulnerability
    user = conn.execute(f'SELECT * FROM users WHERE username = "{username}"').fetchone()
    conn.close()
    return f'User: {user["username"]}, Email: {user["email"]}' if user else 'User not found'

# Vulnerable endpoint: Cross-Site Scripting (XSS)
@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['input']
    # XSS vulnerability
    return render_template_string(f'<h1>Your input: {user_input}</h1>')

if __name__ == '__main__':
    app.run(debug=True)
