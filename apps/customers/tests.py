from rest_framework import status
from rest_framework.test import APITestCase

from apps.customers.models import Customer


class CustomerApiTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            date_of_birth="1995-10-10"
        )

    def test_list_customers_returns_200(self):
        response = self.client.get("/customers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_customer_returns_201(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "date_of_birth": "1998-03-20"
        }

        response = self.client.post("/customers/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(response.data["first_name"], "Jane")

    def test_create_customer_with_invalid_data_returns_400(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "date_of_birth": "199-03-20"
        }

        response = self.client.post("/customers/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_customer_returns_200(self):
        response = self.client.get(f"/customers/{self.customer.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.customer.id)

    def test_get_missing_customer_returns_404(self):
        response = self.client.get("/customers/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer_returns_200(self):
        payload = {
            "first_name": "Johnny",
            "last_name": "Doe",
            "email": "john@example.com",
            "date_of_birth": "1995-10-10"
        }

        response = self.client.put(f"/customers/{self.customer.id}/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, "Johnny")