import pandas as pd
from celery import shared_task
from .models import Customer, Loan
from datetime import datetime

@shared_task
def ingest_customer_data(file_path="customer_data.xlsx"):
    df = pd.read_excel(file_path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row["customer_id"],
            defaults={
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "phone_number": row["phone_number"],
                "monthly_salary": row["monthly_salary"],
                "approved_limit": row["approved_limit"],
                "current_debt": row["current_debt"]
            }
        )


@shared_task
def ingest_loan_data(file_path="loan_data.xlsx"):
    df = pd.read_excel(file_path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row["customer_id"])
            Loan.objects.update_or_create(
                loan_id=row["loan_id"],
                defaults={
                    "customer": customer,
                    "loan_amount": row["loan_amount"],
                    "tenure": row["tenure"],
                    "interest_rate": row["interest_rate"],
                    "monthly_installment": row["monthly_repayment"],
                    "emis_paid_on_time": row["emis_paid_on_time"],
                    "start_date": pd.to_datetime(row["start_date"]),
                    "end_date": pd.to_datetime(row["end_date"]),
                }
            )
        except Customer.DoesNotExist:
            continue

