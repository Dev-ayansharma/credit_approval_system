from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ['customer_id', 'approved_limit']
       

class LoanSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(source='customer.customer_id', read_only=True)
    

    class Meta:
        model = Loan
        fields = "__all__"

class LoanDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = "__all__"
