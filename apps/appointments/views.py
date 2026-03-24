from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from apps.customers.models import Customer
from apps.appointments.models import Appointment
from apps.appointments.serializers import AppointmentSerializer


@api_view(["GET", "POST"])
def appointments(request):
    if request.method == "GET":
        return list_appointments(request)
    return create_appointment(request)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def appointment_detail(request, appointment_id):
    if request.method == "GET":
        return get_appointment(appointment_id)

    if request.method == "PUT":
        return update_appointment(appointment_id, request.data)

    if request.method == "PATCH":
        return partial_update_appointment(appointment_id, request.data)

    return delete_appointment(appointment_id)


@api_view(["GET"])
def customer_appointments(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    appointment_list = Appointment.objects.filter(customer=customer)
    serializer = AppointmentSerializer(appointment_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def list_appointments(request):
    appointment_list = Appointment.objects.all()

    customer_id = request.query_params.get("customer_id")
    status_value = request.query_params.get("status")

    if customer_id is not None:
        appointment_list = appointment_list.filter(customer_id=customer_id)

    if status_value is not None:
        appointment_list = appointment_list.filter(status=status_value)

    serializer = AppointmentSerializer(appointment_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def create_appointment(request):
    serializer = AppointmentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def get_appointment(pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data, status=status.HTTP_200_OK)


def update_appointment(pk, data):
    appointment = get_object_or_404(Appointment, pk=pk)
    serializer = AppointmentSerializer(appointment, data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


def partial_update_appointment(pk, data):
    appointment = get_object_or_404(Appointment, pk=pk)
    serializer = AppointmentSerializer(appointment, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


def delete_appointment(pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)