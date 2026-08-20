from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from review_app.models import Review

User = get_user_model()

class CustomerReviewUpdateTests(APITestCase):

    def setUp(self):
        self.review_author = User.objects.create_user(
            username="customer_user",
            password="Testpassword123!",
            type="customer",
        )

        self.business_user = User.objects.create_user(
            username="business_user",
            password="Testpassword123!",
            type="business",
        )

        self.review = Review.objects.create(
            reviewer=self.review_author,
            business_user=self.business_user,
            rating=4,
            description="Good job",
        )

    def test_review_author_can_update_own_review(self):
        self.client.force_authenticate(user=self.review_author)

        update_data = {
            "rating": 5,
            "description": "Super job",
        }

        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            update_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.description, "Super job")


    def test_other_customer_can_not_update_review(self):
        other_customer = User.objects.create_user(
            username="other_customer",
            password="Testpassword123!",
            type="customer",
        )

        self.client.force_authenticate(user=other_customer)

        update_data = {
            "rating": 1,
            "description": "Changed by another customer",
        }

        response = self.client.patch(
            f"/api/reviews/{self.review.id}/",
            update_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.description, "Good job")


    def test_review_author_can_delete_own_review(self):
        self.client.force_authenticate(user=self.review_author)
        response = self.client.delete(f"/api/reviews/{self.review.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
