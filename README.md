# Employee Nexus 🏢

A comprehensive Flask web application with automated CI/CD pipeline for complete employee management and attendance tracking.

## 🚀 Live Demo

Production Application: employee-nexus-docker-env.eba-42cdhvu8.eu-north-1.elasticbeanstalk.com

## ✨ Features

### Core Business Features

🏢 Employee Management - Comprehensive employee profile and data management
⏰ Attendance Tracking - Real-time clock in/out with automated time calculations
📊 Dashboard Analytics - Interactive attendance monitoring and reporting
🔐 Authentication System - Secure login with OTP verification
👥 User Management - Role-based access control and user administration
📈 Attendance History - Detailed historical attendance records
🕐 Real-time Status - Live employee status tracking

### Technical Features

🐍 Flask Web Framework - Modern Python web development
🐳 Docker Containerization - Consistent deployment across environments
⚡ GitHub Actions CI/CD - Automated testing and deployment pipeline
☁️ AWS Elastic Beanstalk - Scalable cloud hosting
🔄 Automatic Deployment - Zero-downtime deployments on push
📊 Health Monitoring - Application status and performance tracking
🔒 Secure Configuration - Environment-based security settings
🗄️ Modular Database - Organized data layer with separation of concerns

## 🛠 Tech Stack

Backend: Python, Flask
Database: MySQL with custom data access layer
Containerization: Docker
CI/CD: GitHub Actions
Cloud: AWS Elastic Beanstalk
Frontend: HTML5, CSS3, JavaScript, Bootstrap 5
Security: Werkzeug password hashing, Flask-Login, OTP Verification, Session Management
Email Service: SMTP with Gmail integration

## 📁 Project Structure

employee_nexus/
├── .github/
│ └── workflows/
│ └── deploy.yml # GitHub Actions CI/CD pipeline
├── app/ # Main Flask application
│ ├── **init**.py # App factory and configuration
│ ├── config.py # Application configuration
│ ├── attendance/ # Attendance management module
│ │ ├── **init**.py
│ │ ├── forms.py # Attendance forms and validation
│ │ └── routes.py # Clock in/out, dashboard routes
│ ├── authentication/ # User authentication module
│ │ ├── **init**.py
│ │ ├── forms.py # Login, forgot password, OTP forms
│ │ └── routes.py # Auth routes and session management
│ ├── db_models/ # Database layer (Data Access Layer)
│ │ ├── **init**.py
│ │ ├── attendance_db.py # Attendance data operations
│ │ ├── auth_db.py # Authentication data operations
│ │ ├── base_db.py # Database connection and base operations
│ │ ├── employee_db.py # Employee data operations
│ │ └── verify_otp_db.py # OTP verification operations
│ ├── employee/ # Employee management module
│ │ ├── **init**.py
│ │ ├── forms.py # Employee registration forms
│ │ └── routes.py # Employee CRUD operations
│ ├── static/ # Static assets
│ │ ├── css/ # Stylesheets
│ │ ├── js/ # JavaScript files
│ │ └── images/ # Image assets
│ └── templates/ # Jinja2 HTML templates
│ ├── attendance/ # Attendance-related templates
│ ├── auth/ # Authentication templates
│ ├── employee/ # Employee management templates
│ ├── base.html # Base template
│ ├── 404.html # Error pages
│ ├── 403.html
│ └── 500.html
├── .dockerignore # Docker ignore rules
├── .gitignore # Git ignore rules
├── .env # Environment variables (not in repo)
├── Dockerfile # Docker container configuration
├── requirements.txt # Python dependencies
├── requirements-docker.txt # Production Docker dependencies
├── run.py # Application entry point
└── README.md # Project documentation

## 🗄️ Database Schema

### Employee Management

1. Employee profiles with comprehensive personal and professional information
2. Unique employee ID generation and management
3. Role-based data organization

### Authentication System

1. Secure user credentials with password hashing
2. Session management with Flask sessions
3. OTP verification for password reset functionality

### Attendance Tracking

1. Real-time clock in/out records
2. Automated time duration calculations
3. Historical attendance data with date-based queries
4. Daily and weekly attendance summaries

-> Database Platform: MySQL

## 🗄️ AWS RDS MySQL Setup

### Production Database Configuration

This application uses AWS RDS MySQL as the production database for scalability, reliability, and managed maintenance.

1. Create RDS MySQL Instance
2. Configure Security Group
3. Database Schema Setup

   #Connect to RDS MySQL:

   ```bash
   mysql -h employee-nexus-db.ctqyu00myxw1.eu-north-1.rds.amazonaws.com -u admin -p
   ```

   #Create Database Schema:

   ```bash
   -- Create the main database
   CREATE DATABASE employee_nexus;
   USE employee_nexus;

   -- Employee details table
   CREATE TABLE employee_details (
       employee_id VARCHAR(50) PRIMARY KEY,
       salutation VARCHAR(10),
       first_name VARCHAR(100) NOT NULL,
       middle_name VARCHAR(100),
       last_name VARCHAR(100) NOT NULL,
       date_of_birth DATE,
       joined_on DATE,
       post VARCHAR(200),
       mobile_number VARCHAR(15),
       email_id VARCHAR(100) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Attendance records table
   CREATE TABLE attendance_records (
       id INT AUTO_INCREMENT PRIMARY KEY,
       employee_id VARCHAR(50) NOT NULL,
       date DATE NOT NULL,
       clock_in_time DATETIME,
       clock_out_time DATETIME,
       total_hours DECIMAL(4,2),
       status VARCHAR(20) DEFAULT 'present',
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (employee_id) REFERENCES employee_details(employee_id)
   );

   -- Password reset OTPs table
   CREATE TABLE password_reset_otps (
       id INT AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(100) NOT NULL,
       otp_code VARCHAR(10) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       expires_at TIMESTAMP NOT NULL,
       is_used BOOLEAN DEFAULT FALSE
   );

   -- Verify tables creation
   SHOW TABLES;
   ```

4. Environment Variables Configuration
5. Database Connection Code
   #Application Configuration (`app/config.py` and `app/db_models/base_db.py`)
   -> Your application uses a clean architecture where:
   - `config.py` reads environment variables from AWS
   - `base_db.py` uses Flask configuration for database connections

## RDS Management Commands

### Connection Testing:

```bash
# Test RDS connection
mysql -h employee-nexus-db.ctqyu00myxw1.eu-north-1.rds.amazonaws.com -u admin -p

# Check database status
SELECT VERSION();
SHOW DATABASES;
```

## 🚦 Getting Started

### Prerequisites

Python 3.9+ - Core runtime environment
pip - Python package manager
Docker Desktop - For containerized development
Git - Version control system
MySQL - Database server
Gmail Account - For email functionality (SMTP)

## Local Development setup

### Clone the repository

```bash
git clone https://github.com/amisasamal/employee_nexus.git
cd employee_nexus
```

### Create virtual environment

```bash
python -m venv .venv
```

#### Windows

.venv\Scripts\activate

#### macOS/Linux

source .venv/bin/activate

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python run.py
```

### Access the application

Open browser: http://localhost:5000

## Docker Development

### Build Docker image

```bash
docker build -t employee-nexus .
```

### Run container

```bash
docker run -p 5000:5000 employee-nexus
```

## 🐳 Docker Configuration

The application is containerized using Docker for consistent deployment across environments.
Build and run locally:

```bash
docker build -t employee-nexus .
docker run -p 5000:5000 employee-nexus
```

### Access the application

Open browser: http://localhost:5000

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for automated deployment to AWS Elastic Beanstalk.

### Workflow Trigger

Automatic: Push to main branch
Manual: Workflow dispatch from GitHub Actions tab

### Deployment Process

📝 Code pushed to GitHub repository
🔄 GitHub Actions triggered automatically
📦 Application packaged built and tested
🚀 Deployed to AWS Elastic Beanstalk
✅ Live application updated with zero downtime

### Pipeline Configuration

The deployment pipeline is configured in .github/workflows/deploy.yml and includes:

1. Environment setup
2. Dependency installation
3. Application packaging
4. AWS deployment with proper credentials

## ☁️ AWS Deployment Architecture

### Infrastructure Details

Platform: AWS Elastic Beanstalk
Environment: employee-nexus-docker-env
Region: eu-north-1
Instance Type: t3.micro

### Deployment Configuration

The application is deployed using Docker containers on AWS Elastic Beanstalk, providing:

1. Automatic scaling based on traffic
2. Health monitoring and automatic recovery
3. Rolling deployments for zero downtime
4. SSL/TLS termination at load balancer

## 🔍 API Endpoints

### Core Application

/ - GET - Application home page and employee registration
/submit - POST - Employee registration form submission
/health - GET - Health check endpoint for monitoring

### Authentication System

/auth/login - GET, POST - User login with credential validation
/auth/logout - POST - Secure user logout and session cleanup
/auth/forgot-password - GET, POST - Initiate password reset process
/auth/verify-otp - GET, POST - OTP verification for password reset
/auth/resend-otp - POST- Resend OTP for verification/auth/reset-password-verified/<token> - GET, POST - Reset password after OTP verification

### Employee Management

/employee/dashboard - GET - Employee dashboard with profile information

### Attendance Management

/attendance/dashboard - GET- Attendance dashboard with current status
/attendance/clock-in - POST - Record employee clock-in time
/attendance/clock-out - POST - Record employee clock-out time

### Health Check

```bash
curl https://employee-nexus-docker-env.eba-42cdhvu8.eu-north-1.elasticbeanstalk.com/health
```

## 🚀 Deployment Guide

### Automatic Deployment

The easiest way to deploy is through the automated CI/CD pipeline:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

The GitHub Actions workflow will automatically deploy your changes to AWS.

## Manual Deployment(AWS EB CLI)

If you have AWS EB CLI installed:

```bash
eb deploy
```

## 🔧 Development Workflow

### Adding New Features

1. Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

2. Develop your feature following the existing structure:

- Add database models in db_models/
- Create forms in appropriate module forms.py
- Add routes in module routes.py
- Create templates in templates/

3. Test locally

```bash
python run.py
or
docker build -t employee-nexus . && docker run -p 5000:5000 employee-nexus
```

4. Commit and push

```bash
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name
```

5. Create a Pull Request on GitHub

## Installing New Dependencies

```bash
# Install new package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# For Docker dependencies
pip freeze > requirements-docker.txt
```

## 📊 Monitoring and Maintenance

### Application Health Monitoring

Health Endpoint: /health- Returns application status
AWS Console: Monitor through Elastic Beanstalk dashboard
GitHub Actions: Track deployment status and history

### Checking Application Logs

```bash
# AWS EB CLI logs
eb logs --all

# Docker container logs
docker logs <container_id>

# Check running containers
docker ps

# Follow logs in real-time
docker logs -f <container_id>
```

## 🔧 Troubleshooting

## Common Issues and Solutions

### Application won't start locally:

```bash
#Check Python version
python --version

# Verify virtual environment is activated
which python

# Check if all dependencies are installed
pip list

# Verify environment variables
echo $SECRET_KEY  # Linux/Mac
echo %SECRET_KEY% # Windows
```

### Database connection issues:

```bash
# Test MySQL connection
mysql -h localhost -u your_username -p

# Check if database exists
SHOW DATABASES;
```

### Check application status:

```bash
curl http://localhost:5000/health
```

### Rebuild Docker image:

```bash
docker build --no-cache -t employee-nexus .
```

### View Docker images:

```bash
docker images
```

### Remove Docker containers:

```bash
docker rm $(docker ps -aq)
```

### View Git status:

```bash
git status
git log --oneline
```

### Reset local changes:

```bash
git reset --hard HEAD
git clean -fd
```

## 🔒 Security

### Implemented Security Measures

1. Environment Variables: Sensitive data stored in environment variables
2. Password Hashing: Werkzeug secure password hashing
3. Session Management: Flask secure session handling
4. OTP Verification: Time-based one-time passwords for password reset
5. CSRF Protection: Flask-WTF CSRF tokens on all forms
6. Input Validation: Comprehensive form validation and sanitization

### Security Configuration

1. GitHub Secrets for CI/CD credentials
2. AWS IAM roles with minimal required permissions
3. Non-root Docker containers
4. Secure email configuration with app passwords

## 🤝 Contributing

1. Fork the repository on GitHub
2. Create a feature branch from main
3. Make your changes following our coding standards
4. Add tests for new functionality
5. Update documentation as needed
6. Test locally to ensure everything works
7. Submit a pull request with a clear description

## 🙏 Acknowledgments

1. Flask community for the excellent web framework
2. AWS for reliable cloud infrastructure
3. GitHub Actions for seamless CI/CD
4. Bootstrap for responsive UI components

## 📄 License

This project is licensed under the MIT License.

Built with ❤️ using Flask, Docker, and AWS
