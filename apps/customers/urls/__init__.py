from django.urls import path, include

app_name = 'customers'
urlpatterns = [
    path('', include('apps.customers.urls.customer')),
]
