from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.customers.serializers.customer import CustomerSerializer
from apps.customers.services.customer import (
    create_customer as create_customer_service,
    get_customer as get_customer_service,
    list_customers as list_customers_service,
)


@api_view(["GET", "POST"])
def customers(request):
    if request.method == "POST":
        return create_customer(request)
    return list_customers()

@api_view(["GET", "PUT"])
def customer(request, customer_id):
    if request.method == "GET":
        customer_data = get_customer(customer_id)
        return Response(customer_data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_customer(pk):
    customer_data = get_customer_service(pk)
    response_serializer = CustomerSerializer(customer_data)
    return response_serializer.data

def list_customers():
    customers_data = list_customers_service()
    serializer = CustomerSerializer(customers_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = create_customer_service(serializer.validated_data)

    response_serializer = CustomerSerializer(data)

    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
