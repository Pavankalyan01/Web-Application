from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_key"

# Function to create database table
def create_table():
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL,
                 age INTEGER NOT NULL,
                 dob DATE NOT NULL)''')
    conn.commit()
    conn.close()

create_table()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Add user route
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    dob = request.form['dob']

    if not (name and email and age and dob):
        return "All fields are required"
    try:
        age = int(age)
        if age <= 0:
            raise ValueError("Age must be a positive integer")
    except ValueError:
        return "Age must be a positive integer"

    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, age, dob) VALUES (?, ?, ?, ?)", (name, email, age, dob))
    conn.commit()
    conn.close()
    return redirect('/')

# Display users route
@app.route('/users')
def display_users():
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
