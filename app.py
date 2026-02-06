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
    """Student dashboard - Main page with service cards"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    return render_template('student_dashboard.html')

@app.route('/student/my-requests')
@login_required
def my_requests():
    """View all student requests"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    from models import init_models
    Student, _, ServiceRequest = init_models(db)
    
    # Get all student's requests
    requests = ServiceRequest.query.filter_by(student_id=current_user.id).order_by(
        ServiceRequest.submitted_at.desc()
    ).all()
    
    # Calculate statistics
    total_requests = len(requests)
    pending_requests = len([r for r in requests if r.status == 'In Progress'])
    ready_requests = len([r for r in requests if r.status == 'Ready'])
    collected_requests = len([r for r in requests if r.status == 'Collected'])
    
    return render_template('my_requests.html',
                         requests=requests,
                         total_requests=total_requests,
                         pending_requests=pending_requests,
                         ready_requests=ready_requests,
                         collected_requests=collected_requests)

@app.route('/student/calendar')
@login_required
def academic_calendar():
    """Academic calendar page"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    return render_template('academic_calendar.html')

@app.route('/student/faculty')
@login_required
def faculty_details():
    """Faculty details page"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    return render_template('faculty_details.html')

@app.route('/student/apply/<service_type>')
@login_required
def apply_service(service_type):
    """Display application form for specific service"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    service_config = {
        'bonafide': {
            'name': 'Bonafide Certificate',
            'description': 'Certificate for bank, visa, or other official purposes',
            'icon': 'fas fa-certificate'
        },
        'transfer': {
            'name': 'Leaving Certificate',
            'description': 'Transfer certificate for college change or other purposes',
            'icon': 'fas fa-exchange-alt'
        },
        'railway': {
            'name': 'Railway Concession',
            'description': 'Apply for monthly or quarterly railway pass',
            'icon': 'fas fa-train'
        },
        'scholarship': {
            'name': 'Scholarship Application',
            'description': 'Apply for government or institutional scholarships',
            'icon': 'fas fa-graduation-cap'
        },
        'exam': {
            'name': 'Exam Form',
            'description': 'Submit examination registration form',
            'icon': 'fas fa-edit'
        },
        'library': {
            'name': 'Library Card',
            'description': 'Apply for new or renew existing library card',
            'icon': 'fas fa-book'
        },
        'id_card': {
            'name': 'Digital ID Card',
            'description': 'Request or download digital student ID card',
            'icon': 'fas fa-id-card'
        }
    }
    
    if service_type not in service_config:
        flash('Invalid service type!', 'error')
        return redirect(url_for('student_dashboard'))
    
    config = service_config[service_type]
    
    return render_template('apply_service.html',
                         service_type=service_type,
                         service_name=config['name'],
                         service_description=config['description'],
                         service_icon=config['icon'])

@app.route('/student/submit/<service_type>', methods=['POST'])
@login_required
def submit_application(service_type):
    """Handle service application submission"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    from models import init_models
    import os
    from werkzeug.utils import secure_filename
    
    Student, _, ServiceRequest = init_models(db)
    
    try:
        # Handle file uploads
        upload_folder = os.path.join(app.root_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        def save_file(file_field):
            if file_field and file_field.filename:
                filename = secure_filename(file_field.filename)
                # Add timestamp to filename to make it unique
                import time
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(upload_folder, filename)
                file_field.save(filepath)
                return filename
            return None
        
        # Save uploaded files
        id_proof_filename = save_file(request.files.get('id_proof'))
        photo_filename = save_file(request.files.get('photo'))
        fee_receipt_filename = save_file(request.files.get('fee_receipt'))
        additional_doc_filename = save_file(request.files.get('additional_doc'))
        
        # Generate token number
        token = ServiceRequest.generate_token_number(service_type)
        
        # Create service request
        service_request = ServiceRequest(
            student_id=current_user.id,
            request_type=service_type,
            token_number=token,
            status='Submitted',
            id_proof_path=id_proof_filename,
            photo_path=photo_filename,
            fee_receipt_path=fee_receipt_filename,
            additional_doc_path=additional_doc_filename
        )
        
        # Add service-specific fields
        if service_type == 'railway':
            service_request.from_station = request.form.get('from_station')
            service_request.to_station = request.form.get('to_station')
            service_request.journey_class = request.form.get('journey_class')
            service_request.duration = request.form.get('duration')
            service_request.address = request.form.get('address')
        elif service_type in ['bonafide', 'transfer', 'scholarship', 'exam', 'library', 'id_card']:
            service_request.purpose = request.form.get('purpose')
            if service_type == 'transfer':
                # Store last attendance date in remarks
                last_date = request.form.get('last_attendance_date')
                service_request.remarks = f"Last Attendance Date: {last_date}"
            if service_type == 'scholarship':
                annual_income = request.form.get('annual_income')
                service_request.remarks = f"Annual Income: Rs. {annual_income}"
            if service_type == 'exam':
                semester = request.form.get('semester')
                service_request.remarks = f"Semester: {semester}"
            if service_type in ['bonafide', 'id_card']:
                service_request.address = request.form.get('address')
        
        # Add general remarks if provided
        general_remarks = request.form.get('remarks', '').strip()
        if general_remarks:
            if service_request.remarks:
                service_request.remarks += f"\nAdditional: {general_remarks}"
            else:
                service_request.remarks = general_remarks
        
        # Save to database
        db.session.add(service_request)
        db.session.commit()
        
        flash(f'Application submitted successfully! Your token number is: {token}', 'success')
        return redirect(url_for('my_requests'))
        
    except Exception as e:
        db.session.rollback()
        print(f"Error submitting application: {e}")
        flash('An error occurred while submitting your application. Please try again.', 'error')
        return redirect(url_for('apply_service', service_type=service_type))

@app.route('/student/fee-receipts')
@login_required
def fee_receipts():
    """Fee receipts page"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    return render_template('fee_receipts.html')

@app.route('/student/request/<int:request_id>')
@login_required
def request_details(request_id):
    """View complete request details"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    from models import init_models
    _, _, ServiceRequest = init_models(db)
    
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    # Ensure student can only view their own requests
    if service_request.student_id != current_user.id:
        flash('Access denied!', 'error')
        return redirect(url_for('student_dashboard'))
    
    # Service type mapping
    service_names = {
        'bonafide': 'Bonafide Certificate',
        'transfer': 'Transfer Certificate',
        'railway': 'Railway Concession',
        'scholarship': 'Scholarship Application',
        'exam': 'Exam Form',
        'fee': 'Fee Receipt Request',
        'library': 'Library Card',
        'id_card': 'Digital ID Card'
    }
    
    service_icons = {
        'bonafide': 'fas fa-certificate',
        'transfer': 'fas fa-exchange-alt',
        'railway': 'fas fa-train',
        'scholarship': 'fas fa-graduation-cap',
        'exam': 'fas fa-edit',
        'fee': 'fas fa-file-invoice-dollar',
        'library': 'fas fa-book',
        'id_card': 'fas fa-id-card'
    }
    
    # Status timeline - determine which statuses are active
    status_timeline = {
        'submitted': service_request.status in ['Submitted', 'In Progress', 'Ready', 'Collected'],
        'in_progress': service_request.status in ['In Progress', 'Ready', 'Collected'],
        'ready': service_request.status in ['Ready', 'Collected'],
        'collected': service_request.status == 'Collected'
    }
    
    return render_template('request_details.html',
                         request=service_request,
                         service_name=service_names.get(service_request.request_type, service_request.request_type),
                         service_icon=service_icons.get(service_request.request_type, 'fas fa-file'),
                         status_timeline=status_timeline,
                         student=current_user)

@app.route('/student/profile')
@login_required
def student_profile():
    """Student profile page - To be implemented later"""
    if session.get('user_type') != 'student':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    return f"""
    <h1>Student Profile</h1>
    <p>Name: {current_user.full_name}</p>
    <p>Roll Number: {current_user.roll_number}</p>
    <p>Email: {current_user.email}</p>
    <p>Department: {current_user.department}</p>
    <p>Year: {current_user.year}</p>
    <p>Division: {current_user.division}</p>
    <a href='/student/dashboard'>Back to Dashboard</a>
    """

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
