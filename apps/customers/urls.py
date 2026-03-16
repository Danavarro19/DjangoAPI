from django.urls import path
from apps.customers.views import customers, customer_detail

urlpatterns = [
    path('', customers, name='all_customers'),
    path('<int:customer_id>/', customer_detail, name='get_customer')
]
