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

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user based on user type stored in session"""
    from models import init_models
    Student, Worker, _ = init_models(db)
    user_type = session.get('user_type')
    if user_type == 'student':
        return Student.query.get(int(user_id))
    elif user_type == 'worker':
        return Worker.query.get(int(user_id))
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

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/student/register', methods=['POST'])
def student_register():
    """Student registration"""
    try:
        # Import models
        from models import init_models
        Student, _, _ = init_models(db)
        
        # Get form data
        full_name = request.form.get('full_name')
        roll_number = request.form.get('roll_number').upper()
        email = request.form.get('email').lower()
        department = request.form.get('department')
        year = request.form.get('year')
        division = request.form.get('division')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth') + '?role=student')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return redirect(url_for('auth') + '?role=student')
        
        # Check if student already exists
        if Student.query.filter_by(roll_number=roll_number).first():
            flash('Roll number already registered!', 'error')
            return redirect(url_for('auth') + '?role=student')
        
        if Student.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('auth') + '?role=student')
        
        # Create new student
        student = Student(
            full_name=full_name,
            roll_number=roll_number,
            email=email,
            department=department,
            year=year,
            division=division,
            phone_number=phone_number
        )
        student.set_password(password)
        
        db.session.add(student)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth') + '?role=student')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Registration failed: {str(e)}', 'error')
        return redirect(url_for('auth') + '?role=student')

@app.route('/student/login', methods=['POST'])
def student_login():
    """Student login"""
    try:
        from models import init_models
        Student, _, _ = init_models(db)
        
        login_id = request.form.get('login_id')
        password = request.form.get('password')
        
        # Find student by roll number or email
        student = Student.query.filter(
            (Student.roll_number == login_id.upper()) | 
            (Student.email == login_id.lower())
        ).first()
        
        if student and student.check_password(password):
            login_user(student)
            session['user_type'] = 'student'
            flash('Login successful!', 'success')
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
            return redirect(url_for('auth') + '?role=student')
            
    except Exception as e:
        flash(f'Login failed: {str(e)}', 'error')
        return redirect(url_for('auth') + '?role=student')

@app.route('/worker/register', methods=['POST'])
def worker_register():
    """Worker registration"""
    try:
        from models import init_models
        _, Worker, _ = init_models(db)
        
        # Get form data
        full_name = request.form.get('full_name')
        employee_id = request.form.get('employee_id').upper()
        email = request.form.get('email').lower()
        department = request.form.get('department')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth') + '?role=worker')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return redirect(url_for('auth') + '?role=worker')
        
        # Check if worker already exists
        if Worker.query.filter_by(employee_id=employee_id).first():
            flash('Employee ID already registered!', 'error')
            return redirect(url_for('auth') + '?role=worker')
        
        if Worker.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('auth') + '?role=worker')
        
        # Create new worker
        worker = Worker(
            full_name=full_name,
            employee_id=employee_id,
            email=email,
            department=department,
            phone_number=phone_number,
            role='worker',
            is_active=True
        )
        worker.set_password(password)
        
        db.session.add(worker)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth') + '?role=worker')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Registration failed: {str(e)}', 'error')
        return redirect(url_for('auth') + '?role=worker')

@app.route('/worker/login', methods=['POST'])
def worker_login():
    """Worker login"""
    try:
        from models import init_models
        _, Worker, _ = init_models(db)
        
        login_id = request.form.get('login_id')
        password = request.form.get('password')
        
        # Find worker by employee ID or email
        worker = Worker.query.filter(
            (Worker.employee_id == login_id.upper()) | 
            (Worker.email == login_id.lower())
        ).first()
        
        if worker and worker.check_password(password) and worker.is_active:
            login_user(worker)
            session['user_type'] = 'worker'
            flash('Login successful!', 'success')
            return redirect(url_for('worker_dashboard'))
        else:
            flash('Invalid credentials or account inactive!', 'error')
            return redirect(url_for('auth') + '?role=worker')
            
    except Exception as e:
        flash(f'Login failed: {str(e)}', 'error')
        return redirect(url_for('auth') + '?role=worker')

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    session.pop('user_type', None)
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# ==================== DASHBOARD ROUTES (Placeholders for Phase 4) ====================

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    """Student dashboard - To be implemented in Phase 4"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    return f"<h1>Welcome to Student Dashboard, {current_user.full_name}!</h1><a href='/logout'>Logout</a>"

@app.route('/worker/dashboard')
@login_required
def worker_dashboard():
    """Worker dashboard - To be implemented in Phase 7"""
    if session.get('user_type') != 'worker':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    return f"<h1>Welcome to Worker Dashboard, {current_user.full_name}!</h1><a href='/logout'>Logout</a>"

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
    with app.app_context():
        # Initialize models with db
        from models import init_models
        Student, Worker, ConcessionRequest = init_models(db)
        
        # Create all tables
        db.create_all()
        print(">> Database tables created successfully!")
        
        # Create default worker if not exists
        if not Worker.query.filter_by(employee_id='ADMIN001').first():
            admin_worker = Worker(
                employee_id='ADMIN001',
                email='admin@college.edu',
                full_name='System Administrator',
                department='Administration',
                role='admin',
                is_active=True
            )
            admin_worker.set_password('admin123')
            db.session.add(admin_worker)
            db.session.commit()
            print(">> Default worker created:")
            print("   Employee ID: ADMIN001")
            print("   Password: admin123")
    
    # Run the application
    print(">> Starting Railway Concession Management System...")
    print(">> Open your browser at: http://localhost:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
