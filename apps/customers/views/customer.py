from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.customers.models.customer import Customer
from apps.customers.serializers.customer import CustomerSerializer


@api_view(["GET"])
def list_customers(request):

    customers = Customer.objects.all()

    serializer = CustomerSerializer(customers, many=True)

    return Response(serializer.data)
