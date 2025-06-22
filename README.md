# Employee Nexus 🏢

A modern Flask web application with automated CI/CD pipeline for employee management.

## 🚀 Live Demo

Production Application: employee-nexus-docker-env.eba-42cdhvu8.eu-north-1.elasticbeanstalk.com

## ✨ Features

🐍 Flask web framework
🐳 Docker containerization
⚡ GitHub Actions CI/CD pipeline
☁️ AWS Elastic Beanstalk deployment
🔄 Automatic deployment on push to main
📊 Health monitoring endpoint
🔒 Secure environment configuration

## 🛠 Tech Stack

Backend: Python, Flask
Containerization: Docker
CI/CD: GitHub Actions
Cloud: AWS Elastic Beanstalk
Database: SQLite (development), PostgreSQL (production ready)

## 🚦 Getting Started

### Prerequisites

Python 3.9+
Docker Desktop
Git

## Local Development

### Clone the repository

```bash
git clone https://github.com/amisasamal/employee_nexus.git
cd employee_nexus
```

### Create virtual environment

```bash
bashpython -m venv .venv
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

### Access the application

Open browser: http://localhost:5000

## 📁 Project Structure

employee_nexus/
├── .github/
│ └── workflows/
│ └── deploy.yml # GitHub Actions CI/CD
├── app/ # Flask application
│ ├── **init**.py
│ ├── routes.py
│ └── templates/
├── .dockerignore
├── .gitignore
├── Dockerfile # Docker configuration
├── requirements.txt # Python dependencies
├── requirements-docker.txt # Production dependencies
├── run.py # Application entry point
└── README.md

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for automated deployment:

### Workflow Trigger

Automatic: Push to main branch
Manual: Workflow dispatch

### Deployment Process

📝 Code pushed to GitHub
🔄 GitHub Actions triggered
📦 Application packaged
🚀 Deployed to AWS Elastic Beanstalk
✅ Live application updated

## 🐳 Docker Configuration

The application is containerized using Docker for consistent deployment across environments.
Build and run locally:

```bash
docker build -t employee-nexus .
docker run -p 5000:5000 employee-nexus
```

## ☁️ AWS Deployment

### Infrastructure

Platform: AWS Elastic Beanstalk
Environment: employee-nexus-docker-env
Region: eu-north-1
Instance Type: t3.micro

## 🔍 API Endpoints

EndpointMethodDescription/GETHome page/healthGETHealth check endpoint

### Health Check

```bash
curl https://employee-nexus-docker-env.eba-42cdhvu8.eu-north-1.elasticbeanstalk.com/health
```

## 🚀 Deployment

Automatic Deployment
Simply push to the main branch:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

## Manual Deployment

Using AWS EB CLI:

```bash
eb deploy
```

## 🔧 Development

### Adding New Features

Create a feature branch

```bash
git checkout -b feature/your-feature-name
```

### Make your changes

Test locally

```bash
python run.py
or
docker build -t employee-nexus . && docker run -p 5000:5000 employee-nexus
```

### Commit and push

```bash
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name
```

### Create a Pull Request

## Installing New Dependencies

```bash
# Install new package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# For Docker dependencies
pip freeze > requirements-docker.txt
```

## 📊 Monitoring

### Application Health

Health Endpoint: /health
AWS Console: Elastic Beanstalk environment health
GitHub Actions: Deployment status

### Checking Logs

```bash
# AWS EB CLI logs
eb logs

# Docker container logs
docker logs <container_id>

# Check running containers
docker ps
```

## 🔧 Troubleshooting

## Common Commands

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

Environment variables for sensitive data
GitHub Secrets for CI/CD credentials
IAM roles with minimal permissions
Non-root Docker containers

## 🤝 Contributing

Fork the repository
Create a feature branch
Make your changes
Test locally
Submit a pull request

## 📄 License

This project is licensed under the MIT License.

Built with ❤️ using Flask, Docker, and AWS
