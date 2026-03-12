from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.customers.models.customer import Customer
from apps.customers.serializers.customer import CustomerSerializer


@api_view(["GET"])
def list_customers(request):

    customers = Customer.objects.all()

    serializer = CustomerSerializer(customers, many=True)

    return Response(serializer.data)

@api_view(["POST"])
def create_customer(request):

    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)