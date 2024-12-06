from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Simulated database (in-memory)
users = {}

@app.route('/')
def home():
    # If user is already logged in, redirect to the secure page
    if 'username' in session:
        return redirect(url_for('secure_page'))
    # Otherwise, show the login page
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        username = request.form['username']
        password = request.form['password']
        # Check if username already exists
        if username in users:
            flash('Username already exists. Try logging in.', 'error')
            return redirect(url_for('register'))
        # Register the user
        users[username] = password
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('home'))
    # Show the registration page for GET requests
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Fetch form data
        username = request.form['username']
        password = request.form['password']
        # Authenticate user
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('secure_page'))
        flash('Invalid username or password.', 'error')
    # Show the login page for GET requests
    return render_template('login.html')

@app.route('/secure')
def secure_page():
    # Check if user is logged in
    if 'username' in session:
        return render_template('secure.html', username=session['username'])
    flash('You need to log in first.', 'error')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    # Log out the user
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
