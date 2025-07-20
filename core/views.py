from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer, LoanDetailSerializer
from django.db.models import Sum

@api_view(["POST"])
def register_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        monthly_salary = serializer.validated_data['monthly_salary']    
        serializer.save(approved_limit=round(36 * monthly_salary, -5))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def check_loan_eligibility(request):
    customer_id = request.data.get("customer_id")
    loan_amount = float(request.data.get("loan_amount"))
    interest_rate = float(request.data.get("interest_rate"))
    tenure = int(request.data.get("tenure"))

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

    # Simplified Eligibility Logic
    monthly_installment = (loan_amount * (1 + (interest_rate * tenure) / 100)) / tenure
    existing_loans = Loan.objects.filter(customer=customer)
    existing_emi = existing_loans.aggregate(total=Sum('monthly_installment'))['total'] or 0
    salary_ratio = (monthly_installment + existing_emi) / customer.monthly_salary

    if salary_ratio < 0.5:
        return Response({
            "customer_id": customer.customer_id,
            "eligible": True,
            "approved_limit": customer.approved_limit,
            "interest_rate": interest_rate,
            "tenure": tenure,
            "monthly_installment": round(monthly_installment, 2)
        })
    else:
        return Response({
            "customer_id": customer.customer_id,
            "eligible": False,
            "reason": "EMI to income ratio too high"
        })


@api_view(["POST"])
def create_loan(request):
    serializer = LoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
def get_loans_by_customer(request, customer_id):
    loans = Loan.objects.filter(customer__customer_id=customer_id)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_loan_by_id(request, loan_id):
    try:
        loan = Loan.objects.get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=404)
    
    serializer = LoanDetailSerializer(loan)  
    return Response(serializer.data, status=200)

