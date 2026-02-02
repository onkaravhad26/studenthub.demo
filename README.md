# Railway Concession Management System

A web-based system to streamline the railway concession application process for college students, eliminating long queues and manual paperwork.

## 🎯 Project Overview

This system allows:
- **Students** to apply for railway concessions online, upload documents, and track request status
- **Workers** to manage requests efficiently, update status, and maintain digital records
- **College** to provide better service and reduce administrative overhead

## 🛠️ Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python + Flask
- **Database**: MySQL
- **Authentication**: Flask-Login + Bcrypt

## 📋 Prerequisites

Before running this project, make sure you have:

1. **Python 3.8+** installed
2. **MySQL Server** installed and running
3. **pip** (Python package manager)

## 🚀 Setup Instructions

### 1. Clone or Download the Project

```bash
cd "c:/ONKAR/anti gravity/concession"
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

1. Open MySQL and create a database:

```sql
CREATE DATABASE railway_concession_db;
```

2. Update database credentials in `config.py` if needed:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/railway_concession_db'
```

### 5. Create Environment File

```bash
# Copy the example file
copy .env.example .env

# Edit .env and update your settings
```

### 6. Initialize Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

Or simply run the app (it will create tables automatically):

```bash
python app.py
```

### 7. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 📁 Project Structure

```
concession/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── static/               # CSS, JS, images (to be created)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/            # HTML templates (to be created)
│   ├── index.html
│   ├── auth.html
│   └── ...
└── uploads/              # Uploaded documents (auto-created)
```

## 👥 Default Users

After setup, a default worker account is created:

- **Employee ID**: EMP001
- **Password**: worker123

*Note: Students need to register through the registration page.*

## 🔧 Development Status

### ✅ Phase 1: Foundation (COMPLETED)
- Project structure created
- Flask app configured
- Database models implemented
- Configuration setup

### 🔄 Next Phases
- Phase 2: Landing Page
- Phase 3: Authentication System
- Phase 4: Student Dashboard
- Phase 5: Apply for Concession
- Phase 6: My Requests
- Phase 7: Worker Dashboard
- Phase 8: Request Details
- Phase 9: Profile Page
- Phase 10: Polish & Testing

## 📝 Database Models

### Student
- Roll number, email, password
- Personal details (name, department, year, division)
- Relationship to concession requests

### Worker
- Employee ID, email, password
- Personal details and role
- Process concession requests

### ConcessionRequest
- Token number (auto-generated)
- Journey details
- Status tracking (Submitted → In Progress → Ready → Collected)
- Document storage
- Timestamps

## 🎨 Features

- **Multi-stage Status Tracking**: Submitted → In Progress → Ready → Collected
- **Unique Token Numbers**: Format RC-YYYY-XXXX
- **Daily Limit Counter**: Manage concession quotas
- **Document Upload**: Digital submission of required documents
- **Search & Filter**: Easy request management for workers
- **Dashboard Analytics**: Statistics and insights

## 🔐 Security Features

- Password hashing using Bcrypt
- Session management with Flask-Login
- Role-based access control
- Secure file uploads

## 📞 Support

For issues or questions, contact your development team.

## 📄 License

This project is developed as a college mini-project.

---

**Developed by**: [Your Team Name]  
**College**: [Your College Name]  
**Year**: 2026
