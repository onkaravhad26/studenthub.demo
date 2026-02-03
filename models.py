"""
Database Models for Railway Concession Management System
Models are defined as functions and initialized when needed to avoid circular imports
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Cache for model classes to avoid redefining tables
_models_cache = {}

def init_models(db):
    """Initialize and return all model classes (cached)"""
    # Return cached models if already initialized
    if 'Student' in _models_cache:
        return _models_cache['Student'], _models_cache['Worker'], _models_cache['ConcessionRequest']
    
    # ==================== STUDENT MODEL ====================
    
    class Student(db.Model, UserMixin):
        """Student user model"""
        __tablename__ = 'students'
        
        id = db.Column(db.Integer, primary_key=True)
        roll_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
        email = db.Column(db.String(120), unique=True, nullable=False, index=True)
        password_hash = db.Column(db.String(255), nullable=False)
        
        # Personal Information
        full_name = db.Column(db.String(100), nullable=False)
        department = db.Column(db.String(100), nullable=False)
        year = db.Column(db.String(20), nullable=False)  # FE, SE, TE, BE
        division = db.Column(db.String(10))  # A, B, C, etc.
        phone_number = db.Column(db.String(15))
        
        # Timestamps
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # Relationships
        concession_requests = db.relationship('ConcessionRequest', backref='student', lazy=True, cascade='all, delete-orphan')
        
        def set_password(self, password):
            """Hash and set password"""
            self.password_hash = generate_password_hash(password)
        
        def check_password(self, password):
            """Check if password is correct"""
            return check_password_hash(self.password_hash, password)
        
        def __repr__(self):
            return f'<Student {self.roll_number} - {self.full_name}>'
    
    
    # ==================== WORKER MODEL ====================
    
    class Worker(db.Model, UserMixin):
        """Office worker/staff user model"""
        __tablename__ = 'workers'
        
        id = db.Column(db.Integer, primary_key=True)
        employee_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
        email = db.Column(db.String(120), unique=True, nullable=False, index=True)
        password_hash = db.Column(db.String(255), nullable=False)
        
        # Personal Information
        full_name = db.Column(db.String(100), nullable=False)
        department = db.Column(db.String(100))
        phone_number = db.Column(db.String(15))
        
        # Role and permissions
        role = db.Column(db.String(50), default='worker')  # worker, admin
        is_active = db.Column(db.Boolean, default=True)
        
        # Timestamps
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        def set_password(self, password):
            """Hash and set password"""
            self.password_hash = generate_password_hash(password)
        
        def check_password(self, password):
            """Check if password is correct"""
            return check_password_hash(self.password_hash, password)
        
        def __repr__(self):
            return f'<Worker {self.employee_id} - {self.full_name}>'
    
    
    # ==================== CONCESSION REQUEST MODEL ====================
    
    class ConcessionRequest(db.Model):
        """Railway concession request model"""
        __tablename__ = 'concession_requests'
        
        id = db.Column(db.Integer, primary_key=True)
        token_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
        
        #Foreign Keys
        student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
        processed_by = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=True)
        
        # Journey Details
        from_station = db.Column(db.String(100), nullable=False)
        to_station = db.Column(db.String(100), nullable=False)
        journey_class = db.Column(db.String(20), nullable=False)  # First, Second, Sleeper, etc.
        duration = db.Column(db.String(50), nullable=False)  # Monthly, Quarterly
        
        # Request Status
        status = db.Column(db.String(20), default='Submitted', nullable=False)
        # Status options: 'Submitted', 'In Progress', 'Ready', 'Collected'
        
        # Document Paths (stored as file paths)
        id_proof_path = db.Column(db.String(255))
        fee_receipt_path = db.Column(db.String(255))
        photo_path = db.Column(db.String(255))
        previous_concession_path = db.Column(db.String(255))  # if renewal
        
        # Additional Information
        address = db.Column(db.Text)
        remarks = db.Column(db.Text)  # Worker can add remarks
        
        # Timestamps
        submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
        processed_at = db.Column(db.DateTime)  # When worker starts processing
        ready_at = db.Column(db.DateTime)  # When concession is ready
        collected_at = db.Column(db.DateTime)  # When student collects
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        def __repr__(self):
            return f'<ConcessionRequest {self.token_number} - Status: {self.status}>'
        
        @staticmethod
        def generate_token_number():
            """Generate unique token number in format RC-YYYY-XXXX"""
            year = datetime.now().year
            
            # Get the count of requests this year
            year_start = datetime(year, 1, 1)
            count = ConcessionRequest.query.filter(
                ConcessionRequest.submitted_at >= year_start
            ).count()
            
            # Generate token
            token = f"RC-{year}-{(count + 1):04d}"
            return token
        
        def get_status_color(self):
            """Get color for status badge"""
            colors = {
                'Submitted': 'primary',
                'In Progress': 'warning',
                'Ready': 'success',
                'Collected': 'secondary'
            }
            return colors.get(self.status, 'secondary')
    
    # Cache models before returning
    _models_cache['Student'] = Student
    _models_cache['Worker'] = Worker
    _models_cache['ConcessionRequest'] = ConcessionRequest
    
    return Student, Worker, ConcessionRequest
