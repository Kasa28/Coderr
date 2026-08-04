from django.test import TestCase
from rest_framework.test import APIClient


class RegisterTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.registration_data = {
            "username": "testUser",
            "email": "testuser@user.com",
            "password": "Test123!",
            "repeated_password": "Test123!",
            "type": "customer",
        }

    def test_can_User_register(self):
        response = self.client.post(
            "/api/registration/",
            self.registration_data,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "testUser")
        self.assertIn("token", response.data)

    def test_can_User_login(self):
        self.client.post(
            "/api/registration/",
            self.registration_data,
            format="json",
        )

        login_data = {
            "username": "testUser",
            "password": "Test123!",
        }

        response = self.client.post(
            "/api/login/",
            login_data,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "testUser")
        self.assertIn("token", response.data)