from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
USER_FILE = 'user_file.json'

patient_data = {
    'blood_pressure': {'name': 'Blood pressure - Systolic (mm Hg)', 'value': 117, 'min': 20, 'max': 300, 'change': 0.00},
    'temperature': {'name': 'Body temperature in Celcius', 'value': 32, 'min': 30, 'max': 40, 'change': -4.10},
    'saturation': {'name': 'Blood saturation', 'value': 61, 'min': 0, 'max': 100, 'change': -34.00},
    'glucose': {'name': 'Blood glucose (mg dL)', 'value': 124, 'min': 0, 'max': 350, 'change': 23.00},
    'heart_rate': {'name': 'Resting Heart rate (bpm)', 'value': 190, 'min': 0, 'max': 220, 'change': 89.00}
}

# Function to load users from file
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as file:
        return json.load(file)


# Function to save users to file
def save_users(users):
    with open(USER_FILE, 'w') as file:
        json.dump(users, file, indent=4)


@app.route('/')
def home():
    return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            flash('Username already exists!', 'danger')
            return redirect(url_for('login'))

        users[username] = {'password': password}
        save_users(users)
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))
    return render_template('dashboard.html',vitals=patient_data, username=session['username'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)












#
# # app.py
# from flask import Flask, render_template, session, redirect, url_for
# from functools import wraps
#
# app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'  # Change this to a secure key in production
#
# # Dummy patient data
#
#
# # Login required decorator
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'logged_in' not in session:
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function
#
# @app.route('/')
# @login_required
# def dashboard():
#     return render_template('dashboard.html', vitals=patient_data)
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Add your login logic here
#     session['logged_in'] = True
#     return redirect(url_for('dashboard'))
#
# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))
#
# if __name__ == '__main__':
#     app.run(debug=True)
