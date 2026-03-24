from django.urls import path
from apps.customers.views import customers, customer_detail, customer_appointments, customer_appointment_detail

urlpatterns = [
    path('', customers, name='all_customers'),
    path('<int:customer_id>/', customer_detail, name='get_customer'),
    path("<int:customer_id>/appointments/", customer_appointments),
    path("<int:customer_id>/appointments/<int:appointment_id>", customer_appointment_detail),

]
