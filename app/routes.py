from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Habit
from . import db

main = Blueprint('main', __name__)

# Home route
@main.route('/')
def home():
    return render_template('index.html', user=current_user)

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))  # Redirect to 'main.index' after login
        flash('Invalid username or password')
    return render_template('login.html')

# Dashboard route, requires login
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

# Logout route
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))  # Redirect to 'main.home' after logout
