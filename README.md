# 🏦 LoanGuard

A Flask-based Loan Management System developed as a Database Management System (DBMS) project. LoanGuard streamlines the management of borrowers and loan applications while demonstrating relational database design, SQL programming, and full-stack web development using Flask and MySQL.

---

## 📌 Project Overview

LoanGuard is designed to simulate the workflow of a financial institution managing loan applications. The system allows bank staff to manage borrower information, create loan applications, and monitor application status through a simple web interface backed by a normalized MySQL database.

This project demonstrates:

- Relational Database Design
- Entity-Relationship Modeling (EERD)
- SQL Constraints
- Stored Procedures
- Database Views
- Database Triggers
- Flask Backend Development
- MySQL Integration

---

# ✨ Features

## 👤 Borrower Management

- View all borrowers
- Add new borrowers
- Edit borrower information
- Delete borrowers
- Validation for duplicate Email and NID
- Flash messages for successful and failed operations

---

## 📄 Loan Application Management

- View all loan applications
- Create new loan applications
- Update application status
- Track application details

---

## 🗄 Database Features

- Fully normalized relational schema
- Primary Keys
- Foreign Keys
- CHECK Constraints
- ENUM attributes
- Stored Procedures
- Views
- Triggers
- Sample Seed Data

---

# 🛠 Technologies Used

### Backend

- Python
- Flask
- PyMySQL

### Database

- MySQL
- MySQL Workbench

### Frontend

- HTML5
- Bootstrap 5
- Jinja2 Templates

### Development Tools

- VS Code
- Git
- GitHub

---

# 📂 Project Structure

```
LoanGuard
│
├── backend
│   ├── app.py
│   ├── config.py
│   ├── database
│   │   └── connection.py
│   │
│   ├── routes
│   │   ├── borrower.py
│   │   └── application.py
│   │
│   ├── templates
│   │   ├── base.html
│   │   ├── borrowers.html
│   │   ├── add_borrower.html
│   │   ├── edit_borrower.html
│   │   ├── applications.html
│   │   ├── add_application.html
│   │   └── edit_application.html
│   │
│   └── static
│
├── database
│   ├── schema.sql
│   ├── seed.sql
│   ├── views.sql
│   ├── procedures.sql
│   └── triggers.sql
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🗄 Database Objects

The project contains the following SQL objects:

### Tables

- BORROWER
- BANK_STAFF
- LOAN_APPLICATION
- LOAN
- LOAN_PAYMENT
- CREDIT_ASSESSMENT
- BORROWER_PHONE

### Views

- Applications by borrower
- Loan summary views

### Stored Procedures

- Retrieve applications by status

### Trigger

- Automatically update loan balance after successful payment

---

# ⚙️ Installation

## Clone the repository

```bash
git clone https://github.com/Ahnaf1014/LoanGuard.git
```

```bash
cd LoanGuard
```

---

## Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄 Database Setup

Create a MySQL database.

Execute the SQL files in the following order:

```
schema.sql

↓

seed.sql

↓

views.sql

↓

procedures.sql

↓

triggers.sql
```

Update your database credentials in:

```
backend/config.py
```

or

```
.env
```

depending on your configuration.

---

# ▶️ Running the Application

Navigate to the backend folder:

```bash
cd backend
```

Run the Flask application:

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

> Add screenshots inside:

```
docs/screenshots/
```

Suggested screenshots:

- Dashboard
- Borrower List
- Add Borrower
- Edit Borrower
- Loan Applications
- Add Application
- Update Application Status
- MySQL Database
- ER Diagram

Example:

```markdown
## Borrowers

![Borrowers](docs/screenshots/borrowers.png)
```

---

# 📊 Entity Relationship Diagram

Add your EER Diagram here.

Example:

```markdown
![ER Diagram](docs/screenshots/eerd.png)
```

---

# 🚀 Future Improvements

- User Authentication
- Role-based Access Control
- Loan Approval Workflow
- Payment Dashboard
- Search and Filtering
- Reports and Analytics
- Responsive Dashboard
- File Upload Support
- REST API
- Unit Testing

---

# 📚 Learning Outcomes

This project demonstrates practical knowledge of:

- Database Normalization
- SQL Programming
- Stored Procedures
- Database Triggers
- Views
- Flask Web Development
- Database Connectivity
- CRUD Operations
- Git Version Control

---

# 👨‍💻 Author

**Ahnaf Chowdhury**

Computer Science & Engineering Student

GitHub:
https://github.com/Ahnaf1014

---

# 📄 License

This project was developed for academic purposes as part of a Database Management System (DBMS) course.
