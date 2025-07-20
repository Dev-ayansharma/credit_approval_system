# 🏦 Credit Approval System

A full-stack Django + Celery + PostgreSQL based web application to manage customers and automate loan eligibility checks with background data ingestion.

---

## 🚀 Features

- ✅ **Register Customers** with automatic approved credit limit
- 🧮 **Loan Eligibility Checker** based on salary and EMIs
- 📝 **Create Loans** with interest rate, tenure, and EMI
- 📄 **View Loans** by Customer or Loan ID (with customer details)
- 📥 **Background Ingestion** of customer and loan data from Excel
- ⚙️ **Asynchronous Task Processing** using Celery & Redis
- 🐳 **Dockerized Environment** for seamless deployment

---

## 🛠️ Tech Stack

- **Backend:** Django + Django REST Framework
- **Task Queue:** Celery
- **Database:** PostgreSQL
- **Broker:** Redis
- **Containerization:** Docker + Docker Compose
- **Data Ingestion:** Pandas + Excel files

---

## 📦 Project Structure



credit_approval_system/
├── core/ # App: models, views, tasks, serializers, urls
├── credit_system/ # Django config
├── customer_data.xlsx # Sample customer data
├── loan_data.xlsx # Sample loan data
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env # Environment variables
└── README.md # You're here



---


---

## 📂 Environment Variables

Create a `.env` file in the root:



DATABASE_NAME=creditdb
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_HOST=db
CELERY_BROKER_URL=redis://redis:6379/0



---

## 🐳 Docker Setup

### ✅ Step 1: Clone Repo

```bash
git clone https://github.com/yourusername/credit_approval_system.git
cd credit_approval_system

docker compose up --build

```
The app will be available at http://localhost:8000.


## ⚙️ Run Migrations

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

```

## 🧠 Data Ingestion via Celery

```bash

docker compose exec web python manage.py shell

from core.tasks import ingest_customer_data, ingest_loan_data
ingest_customer_data.delay("customer_data.xlsx")
ingest_loan_data.delay("loan_data.xlsx")

```

### 🔌 API Endpoints

➕ Register Customer
POST /api/register/ 

Request body
{
  "first_name": "Ayan",
  "last_name": "Sharma",
  "phone_number": "9876543210",
  "age": 24,
  "monthly_salary": 50000
}


change data to work

Response:
{
  "customer_id": 1,
  "first_name": "Ayan",
  "last_name": "Sharma",
  "phone_number": "9876543210",
  "age": 24,
  "monthly_salary": 50000,
  "approved_limit": 1800000.0
}


Check Loan Eligibility
POST /api/check-eligibility/

Request:
{
  "customer_id": 1,
  "loan_amount": 200000,
  "interest_rate": 10,
  "tenure": 12
}

Response:
{
  "customer_id": 1,
  "eligible": true,
  "approved_limit": 1800000.0,
  "interest_rate": 10,
  "tenure": 12,
  "monthly_installment": 18333.33
}


📝 Create Loan
POST /api/create-loan/

Request:
{
  "customer": 1,
  "loan_amount": 200000,
  "tenure": 12,
  "interest_rate": 10,
  "monthly_installment": 18333.33,
  "emis_paid_on_time": 10,
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}


📂 Get Loans for a Customer
GET /api/loans/<customer_id>/

Response:
[
  {
    "loan_id": 1,
    "customer": {
      "customer_id": 1,
      "first_name": "Ayan",
      ...
    },
    "loan_amount": 200000,
    "tenure": 12,
    ...
  }
]

🔍 Get Loan by ID
GET /api/loan/<loan_id>/

Response:

{
  "loan_id": 1,
  "customer": {
    "customer_id": 1,
    "first_name": "Ayan",
    ...
  },
  "loan_amount": 200000,
  "tenure": 12,
  ...
}


👨‍💻 Author
Ayan Sharma
Web Developer | Django & React Enthusiast
[My portfolio](https://me-ayansharma.vercel.app/)
[My github](https://github.com/Dev-ayansharma)




