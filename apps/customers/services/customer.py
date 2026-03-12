from django.shortcuts import get_object_or_404

from apps.customers.models import Customer


def list_customers():
    return Customer.objects.all()

def create_customer(data):
    return Customer.objects.create(**data)

def get_customer(pk):
    return get_object_or_404(Customer, pk=pk)
