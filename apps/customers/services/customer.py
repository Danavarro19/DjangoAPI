from apps.customers.models import Customer
from apps.customers.serializers.customer import CustomerSerializer


def list_customers():
    all_customers = Customer.objects.all()
    serializer = CustomerSerializer(all_customers, many=True)

    return serializer.data

def create_customer(data):
    serializer = CustomerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data

    raise Exception(serializer.errors)

