from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer

from apps.appointments.models import Appointment
from apps.appointments.serializers import AppointmentSerializer

@api_view(["GET", "POST"])
def customers(request):
    if request.method == "GET":
        return list_customers(request)
    return create_customer(request)

@api_view(["GET", "PUT"])
def customer_detail(request, customer_id):
    if request.method == "GET":
        return get_customer(customer_id)
    return update_customer(customer_id, request.data)

def get_customer(pk):
    customer = get_object_or_404(Customer, pk=pk)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_200_OK)

def update_customer(pk, data):
    customer = get_object_or_404(Customer, pk=pk)
    serializer = CustomerSerializer(customer, data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

def list_customers(request):
    customer_list = Customer.objects.all()
    serializer = CustomerSerializer(customer_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def customer_appointments(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    appointments = Appointment.objects.filter(customer=customer)

    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def customer_appointment_detail(request, customer_id, appointment_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    try:
        appointment = customer.appointments.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        return Response({"message": "No entry found"},status=status.HTTP_404_NOT_FOUND)
    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data)