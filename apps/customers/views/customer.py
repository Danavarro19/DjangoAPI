from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.customers.models.customer import Customer
from apps.customers.serializers.customer import CustomerSerializer


@api_view(["GET", "POST"])
def customers(request):
    if request.method == "GET":
        return list_customers()
    return create_customer(request)

def list_customers():
    from apps.customers.services.customer import list_customers
    customers_data = list_customers()

    return Response(customers_data)

def create_customer(request):
    from apps.customers.services.customer import create_customer
    try:
        data = create_customer(request.data)
        return Response(data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(e, status=status.HTTP_400_BAD_REQUEST)
