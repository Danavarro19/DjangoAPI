from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.customers.models import Customer
from apps.appointments.models import Appointment


class AppointmentApiTests(APITestCase):
    def setUp(self):
        self.customer_1 = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            date_of_birth="1995-10-10"
        )

        self.customer_2 = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            date_of_birth="1998-03-20"
        )

        self.appointment_1 = Appointment.objects.create(
            customer=self.customer_1,
            scheduled_for=timezone.now() + timezone.timedelta(days=1),
            status="scheduled",
            notes="Initial consultation"
        )

        self.appointment_2 = Appointment.objects.create(
            customer=self.customer_1,
            scheduled_for=timezone.now() + timezone.timedelta(days=2),
            status="completed",
            notes="Follow-up"
        )

        self.appointment_3 = Appointment.objects.create(
            customer=self.customer_2,
            scheduled_for=timezone.now() + timezone.timedelta(days=3),
            status="cancelled",
            notes="Cancelled by customer"
        )

    def test_list_appointments_returns_200(self):
        response = self.client.get("/appointments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_appointments_returns_all_records(self):
        response = self.client.get("/appointments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_appointment_returns_201(self):
        payload = {
            "customer": self.customer_1.id,
            "scheduled_for": (timezone.now() + timezone.timedelta(days=5)).isoformat(),
            "status": "scheduled",
            "notes": "New appointment"
        }

        response = self.client.post("/appointments/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 4)
        self.assertEqual(response.data["customer"], self.customer_1.id)
        self.assertEqual(response.data["status"], "scheduled")

    def test_create_appointment_with_invalid_customer_returns_400(self):
        payload = {
            "customer": 9999,
            "scheduled_for": (timezone.now() + timezone.timedelta(days=5)).isoformat(),
            "status": "scheduled",
            "notes": "Invalid customer"
        }

        response = self.client.post("/appointments/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_appointment_with_invalid_status_returns_400(self):
        payload = {
            "customer": self.customer_1.id,
            "scheduled_for": (timezone.now() + timezone.timedelta(days=5)).isoformat(),
            "status": "bad_status",
            "notes": "Invalid status"
        }

        response = self.client.post("/appointments/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_appointment_returns_200(self):
        response = self.client.get(f"/appointments/{self.appointment_1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.appointment_1.id)

    def test_get_missing_appointment_returns_404(self):
        response = self.client.get("/appointments/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_appointment_returns_200(self):
        payload = {
            "customer": self.customer_1.id,
            "scheduled_for": (timezone.now() + timezone.timedelta(days=10)).isoformat(),
            "status": "completed",
            "notes": "Updated appointment"
        }

        response = self.client.put(
            f"/appointments/{self.appointment_1.id}/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.appointment_1.refresh_from_db()
        self.assertEqual(self.appointment_1.status, "completed")
        self.assertEqual(self.appointment_1.notes, "Updated appointment")

    def test_patch_appointment_returns_200(self):
        payload = {
            "status": "completed"
        }

        response = self.client.patch(
            f"/appointments/{self.appointment_1.id}/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.appointment_1.refresh_from_db()
        self.assertEqual(self.appointment_1.status, "completed")

    def test_delete_appointment_returns_204(self):
        response = self.client.delete(f"/appointments/{self.appointment_1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 2)

    def test_filter_appointments_by_customer_id(self):
        response = self.client.get(f"/appointments/?customer_id={self.customer_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        returned_ids = {item["id"] for item in response.data}
        self.assertIn(self.appointment_1.id, returned_ids)
        self.assertIn(self.appointment_2.id, returned_ids)

    def test_filter_appointments_by_status(self):
        response = self.client.get("/appointments/?status=scheduled")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.appointment_1.id)

    # def test_list_customer_appointments_returns_200(self):
    #     response = self.client.get(f"/customers/{self.customer_1.id}/appointments/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_list_customer_appointments_returns_only_customer_records(self):
    #     response = self.client.get(f"/customers/{self.customer_1.id}/appointments/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 2)
    #
    #     returned_ids = {item["id"] for item in response.data}
    #     self.assertIn(self.appointment_1.id, returned_ids)
    #     self.assertIn(self.appointment_2.id, returned_ids)
    #     self.assertNotIn(self.appointment_3.id, returned_ids)