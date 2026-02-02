"""
Database Models for Railway Concession Management System
"""

from datetime import datetime
from flask_login import UserMixin

# ==================== STUDENT MODEL ====================

class Student(UserMixin):
    """Student user model"""
    
    def __init__(self, db):
        self.db = db
        self.__tablename__ = 'students'
    
    # This is a simplified version - we'll use proper SQLAlchemy in Phase 3


# ==================== WORKER MODEL ====================

class Worker(UserMixin):
    """Office worker/staff user model"""
    
    def __init__(self, db):
        self.db = db
        self.__tablename__ = 'workers'


# ==================== CONCESSION REQUEST MODEL ====================

class ConcessionRequest:
    """Railway concession request model"""
    
    def __init__(self, db):
        self.db = db
        self.__tablename__ = 'concession_requests'
