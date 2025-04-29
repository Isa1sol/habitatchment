from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Habit
from . import db

# Define the main blueprint
main = Blueprint('main', __name__)

# Home page
@main.route('/')
def home():
    return render_template('index.html')  # index.html should have your "Get Started" button

# Register page
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('main.register'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Create new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))

    return render_template('register.html')

# Login page
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('main.login'))

    return render_template('login.html')

# Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))

# Dashboard (only accessible when logged in)
@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        habit_name = request.form['habit_name']
        description = request.form.get('description', '')  # Optional description

        if habit_name:
            new_habit = Habit(name=habit_name, description=description, user_id=current_user.id)
            db.session.add(new_habit)
            db.session.commit()
            flash('Habit added successfully!')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Habit name is required.')

    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', habits=habits)

# Add habit page (accessible when logged in)
@main.route('/add_habit', methods=['GET', 'POST'])
@login_required
def add_habit():
    if request.method == 'POST':
        habit_name = request.form['habit_name']
        description = request.form.get('description', '')  # Optional description
        
        if habit_name:
            new_habit = Habit(name=habit_name, description=description, user_id=current_user.id)
            db.session.add(new_habit)
            db.session.commit()
            flash('Habit added successfully!')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Habit name is required.')

    return render_template('add_habit.html')
