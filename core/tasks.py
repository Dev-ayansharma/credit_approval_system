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
               
            }
        )


from celery import shared_task
from .models import Customer, Loan
import pandas as pd

@shared_task
def ingest_loan_data(file_path="loan_data.xlsx"):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row["Customer ID"])
            Loan.objects.update_or_create(
                loan_id=row["Loan ID"],
                defaults={
                    "customer": customer,
                    "loan_amount": row["Loan Amount"],
                    "tenure": row["Tenure"],
                    "interest_rate": row["Interest Rate"],
                    "monthly_installment": row["Monthly payment"],
                    "emis_paid_on_time": row["EMIs paid on Time"],
                    "start_date": pd.to_datetime(row["Date of Approval"]),
                    "end_date": pd.to_datetime(row["End Date"]),
                }
            )
        except Customer.DoesNotExist:
            continue

