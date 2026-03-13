from django.urls import path
from apps.customers.views import customers, customer


urlpatterns = [
    path('', customers, name='all_customers'),
    path('<int:customer_id>/', customer, name='get_customer')
]
