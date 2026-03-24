from django.urls import path

from apps.appointments.views import (
    appointments,
    appointment_detail,
    customer_appointments,
)


urlpatterns = [
    path('', appointments),
    path('<int:appointment_id>/', appointment_detail),
    # path("customers/<int:customer_id>/appointments/", customer_appointments),
]