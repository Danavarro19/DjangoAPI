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
    all_customers = Customer.objects.all()
    serializer = CustomerSerializer(all_customers, many=True)

    return Response(serializer.data)

def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
