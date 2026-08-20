from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from profile_app.models import Profile

User = get_user_model()

class OnlyGuestLoginTests(APITestCase):

    def test_guest_customer_is_created(self):
        response = self.client.post(
            "/api/guest-login/",
            {"type": "customer"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "guest_customer")
        self.assertIn("token", response.data)

        guest_user = User.objects.get(username="guest_customer")
        self.assertEqual(guest_user.type, "customer")
        self.assertTrue(Profile.objects.filter(user=guest_user).exists())

    def test_guest_business_is_created(self):
        response = self.client.post(
            "/api/guest-login/",
            {"type": "business"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "guest_business")
        self.assertIn("token", response.data)
