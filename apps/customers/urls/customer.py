from django.urls import path
from apps.customers.views import customers


urlpatterns = [
    path('', customers, name='all_customers')
]