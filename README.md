# Employee Management API (FastAPI + MongoDB)

This project is a **RESTful API** built with **FastAPI** and **MongoDB** for managing employees.  
It supports CRUD operations, search, pagination, and schema validation.  

---

## 🚀 Features
- Create, Read, Update, and Delete employees  
- Search employees by skills  
- Get average salary by department  
- Pagination support for employee listing  
- MongoDB schema validation  
- Index on `employee_id` for uniqueness  

---

## 🛠️ Tech Stack
- **Backend:** FastAPI  
- **Database:** MongoDB (using Motor async driver)  
- **Validation:** Pydantic + MongoDB JSON Schema  

---

## 📂 Project Structure
```
employee-management-api/
│── main.py           # FastAPI app with routes
│── requirements.txt  # Python dependencies
│── README.md         # Documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/employee-management-api.git
cd employee-management-api
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup MongoDB
- Start MongoDB locally (default: `mongodb://localhost:27017`)  
- Create database:
```js
use assessment_db
db.createCollection("employees")
```
- Insert some dummy employees:
```js
db.employees.insertMany([
  {
    "employee_id": "E001",
    "name": "Alice",
    "department": "Engineering",
    "salary": 75000,
    "joining_date": new Date("2021-05-15"),
    "skills": ["Python", "FastAPI", "MongoDB"]
  },
  {
    "employee_id": "E002",
    "name": "Bob",
    "department": "HR",
    "salary": 50000,
    "joining_date": new Date("2022-03-10"),
    "skills": ["Recruitment", "Communication"]
  }
])
```

### 4. Run the App
```bash
python main.py
```

By default, it runs on:
```
http://127.0.0.1:8000
```

---

## 📌 API Endpoints

### 👤 Employee CRUD
- **POST** `/employees` → Create employee  
- **GET** `/employees/{employee_id}` → Get employee by ID  
- **PUT** `/employees/{employee_id}` → Update employee  
- **DELETE** `/employees/{employee_id}` → Delete employee  

### 🔎 Advanced Queries
- **GET** `/employees?department=Engineering&skip=0&limit=10` → List employees with pagination  
- **GET** `/employees/search?skill=Python` → Search employees by skill  
- **GET** `/employees/avg-salary` → Average salary by department  

---

## 📖 API Docs
FastAPI provides interactive docs:  

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

---


