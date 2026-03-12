from django.urls import path
from apps.customers.views import list_customers


urlpatterns = [
    path('', list_customers, name='all_customers')
]