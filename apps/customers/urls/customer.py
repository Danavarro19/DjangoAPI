from django.urls import path
from apps.customers.views import get_all


urlpatterns = [
    path('', get_all, name='all_customers')
]