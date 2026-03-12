from rest_framework.serializers import ModelSerializer

from apps.customers.models.customer import Customer


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'