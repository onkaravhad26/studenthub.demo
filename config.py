"""
Configuration Settings for Railway Concession Management System
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-12345'
    
    # Database Configuration
    # Using SQLite for development (change to MySQL for production)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'railway_concession.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL query debugging
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # Stay logged in for 7 days
    SESSION_COOKIE_SECURE = False  # Railway uses HTTPS but set via env var
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_DURATION = timedelta(days=7)  # remember=True lasts 7 days
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    
    # Daily Concession Limit
    DAILY_CONCESSION_LIMIT = 50  # Maximum concessions per day
    
    # Application Settings
    APP_NAME = 'Railway Concession Management System'
    COLLEGE_NAME = 'Your College Name'
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Create upload folder if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
