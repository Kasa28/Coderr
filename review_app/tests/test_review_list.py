from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from review_app.models import Review


User = get_user_model()


class ReviewListTests(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer_user",
            password="Testpassword123!",
            type="customer",
        )

        self.first_business_user = User.objects.create_user(
            username="first_business_user",
            password="Testpassword123!",
            type="business",
        )

        self.second_business_user = User.objects.create_user(
            username="second_business_user",
            password="Testpassword123!",
            type="business",
        )

        self.first_review = Review.objects.create(
            reviewer=self.customer_user,
            business_user=self.first_business_user,
            rating=5,
            description="First review",
        )

        Review.objects.create(
            reviewer=self.customer_user,
            business_user=self.second_business_user,
            rating=3,
            description="Second review",
        )

