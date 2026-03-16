from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer


@api_view(["GET", "POST"])
def customers(request):
    if request.method == "POST":
        return create_customer(request)
    return list_customers(request)

@api_view(["GET", "PUT"])
def customer(request, customer_id):
    if request.method == "GET":
        return get_customer(customer_id)
    if request.method == "PUT":
        return update_customer(customer_id, request.data)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_customer(pk):
    customer_data = get_object_or_404(Customer, pk=pk)
    response_serializer = CustomerSerializer(customer_data)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

def update_customer(pk, data):
    customer_to_update = get_object_or_404(Customer, pk=pk)
    serializer = CustomerSerializer(customer_to_update, data=data)
    serializer.is_valid(raise_exception=True)

    customer_updated = serializer.save()
    response_serializer = CustomerSerializer(customer_updated)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


def list_customers(request):
    customers_data = Customer.objects.all()
    response_serializer = CustomerSerializer(customers_data, many=True)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    customer_new = serializer.save()
    response_serializer= CustomerSerializer(customer_new)

    return Response(response_serializer.data, status=status.HTTP_201_CREATED)

