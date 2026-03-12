from django.db.models import Model, CharField, EmailField, DateField

class Customer(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = EmailField(null=True, blank=True)
    date_of_birth = DateField()

    class Meta:
        app_label = 'customers'
        db_table = 'customers'