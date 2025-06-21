# Employee Nexus

**Employee Nexus** is a Flask-based employee management system designed for easy deployment and scalability.  
It provides features like employee record management, authentication, and role-based access, all containerized using Docker.

---

## 🚀 Features
- User authentication (Login / Logout / Register)
- Employee CRUD (Create, Read, Update, Delete employee records)
- Role-based access (Admin/User)
- Flask modular structure
- Dockerized for seamless deployment
- REST API-ready

---

## ⚙️ Requirements
- Python 3.8+
- Flask
- Docker
- Git

*(All Python dependencies are listed in `requirements.txt`)*

---

## 🐳 Run with Docker
 ### 1️⃣ Build Docker image
 ```bash
 docker build -t employee_nexus .
 ```
 ### 2️⃣ Run Docker container
 ```bash
 docker run -p 5000:5000 employee_nexus
