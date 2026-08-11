from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from profile_app.models import Profile

User = get_user_model()

class ProfileApiTest(APITestCase):

    def test_user_can_get_profile(self):
        user = User.objects.create_user(
            username="max_business",
            email="max@business.de",
            password="testpassword123",
            first_name="Max",
            last_name="Mustermann",
            type="business",
        )

        profile = Profile.objects.create(
            user=user,
            location="Berlin",
            tel="123456789",
            description="Business description",
            working_hours="9-17",
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(
            f"/api/profile/{user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["username"],
            "max_business"
        )

        self.assertEqual(
            response.data["location"],
            "Berlin"
        )


    def test__user_cannot_get_profile(self):
        user = User.objects.create_user(
            username="max_business",
            email="max@business.de",
            password="testpassword123",
            type="business",
        )

        Profile.objects.create(
            user=user,
            location="Berlin",
        )

        response = self.client.get(
            f"/api/profile/{user.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_profile_not_found(self):
        user = User.objects.create_user(
            username="max_business",
            email="max@business.de",
            password="testpassword123",
            type="business",
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(
            "/api/profile/99999/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )