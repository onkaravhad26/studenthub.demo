"""
Railway Concession Management System
Main Flask Application
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
import os
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# User loader for Flask-Login (will implement in Phase 3)
@login_manager.user_loader
def load_user(user_id):
    # To be implemented in Phase 3 with authentication
    return None

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/auth')
def auth():
    """Login/Signup page"""
    return render_template('auth.html')

# Will add more routes in subsequent phases

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ==================== TEMPLATE FILTERS ====================

@app.template_filter('datetime')
def format_datetime(value):
    """Format datetime for display"""
    if value is None:
        return ""
    return value.strftime('%d %b %Y, %I:%M %p')

@app.template_filter('date')
def format_date(value):
    """Format date for display"""
    if value is None:
        return ""
    return value.strftime('%d %b %Y')

# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    # Run the application
    print("🚀 Starting Railway Concession Management System...")
    print("📍 Open your browser at: http://localhost:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
