from django.test import TestCase
from django.contrib.auth import get_user_model
from profile_app.models import Profile
from profile_app.api.serializers import ProfileSerializer

User = get_user_model()

class ProfileSerializerTest(TestCase):

    def test_serializer_returns_user_data(self):
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

        serializer = ProfileSerializer(profile)
        self.assertEqual(serializer.data["username"], "max_business")
        self.assertEqual(serializer.data["first_name"], "Max")
        self.assertEqual(serializer.data["last_name"], "Mustermann")
        self.assertEqual(serializer.data["type"], "business")
        self.assertEqual(serializer.data["email"], "max@business.de")
        self.assertEqual(serializer.data["location"], "Berlin")



    def test_serializer_updates_data(self):
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

        data = {
            "first_name": "Peter",
            "last_name": "Schmidt",
            "email": "peter@example.com",
            "location": "Hamburg",
            "tel": "987654321",
            "description": "Neue Beschreibung",
            "working_hours": "10-18",
        }

        serializer = ProfileSerializer(
            profile,
            data=data,
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        serializer.save()
        user.refresh_from_db()
        profile.refresh_from_db()
        self.assertEqual(user.first_name, "Peter")
        self.assertEqual(user.last_name, "Schmidt")
        self.assertEqual(user.email, "peter@example.com")
        self.assertEqual(profile.location, "Hamburg")
        self.assertEqual(profile.tel, "987654321")
        self.assertEqual(profile.description, "Neue Beschreibung")
        self.assertEqual(profile.working_hours, "10-18")