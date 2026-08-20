from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from review_app.models import Review

User = get_user_model()

class CreateReviewTests(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer_user",
            password="Testpassword123!",
            type="customer",
        )

        self.business_user = User.objects.create_user(
            username="business_user",
            password="Testpassword123!",
            type="business",
        )

    def test_customer_can_create_review(self):
        self.client.force_authenticate(user=self.customer_user)

        new_review_data = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Good job",
        }

        response = self.client.post("/api/reviews/", new_review_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(),1)

        created_review = Review.objects.first()

        self.assertEqual(created_review.reviewer, 
        self.customer_user)
        self.assertEqual(created_review.business_user,
        self.business_user)
        self.assertEqual(created_review.rating, 5)
        self.assertEqual(created_review.description,"Good job")


    def test_business_user_can_not_create_review(self):
        self.client.force_authenticate(user=self.business_user)

        review_data = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Testreview",
        }

        response = self.client.post(
            "/api/reviews/",
            review_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Review.objects.count(),0)


    def test_rating_more_then_is_allowed(self):
        self.client.force_authenticate(user=self.customer_user)

        review_data = {
            "business_user": self.business_user.id,
            "rating": 7,
            "description": "Not allowed more as 5 ",
        }

        response = self.client.post(
            "/api/reviews/",
            review_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 0)


    def test_customer_can_not_review_same_business_twice(self):
        Review.objects.create(
            reviewer=self.customer_user,
            business_user=self.business_user,
            rating=5,
            description="one review",
        )

        self.client.force_authenticate(user=self.customer_user)

        second_review_data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "twice review",
        }

        response = self.client.post(
            "/api/reviews/",
            second_review_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(),1)