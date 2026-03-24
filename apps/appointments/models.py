from django.db import models
from apps.customers.models import Customer

class Appointment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="appointments")
    scheduled_for = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ])
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)