from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_customer),
    path("check-eligibility/", views.check_loan_eligibility),
    path("create-loan/", views.create_loan),
    path("loans/<int:customer_id>/", views.get_loans_by_customer),
]
