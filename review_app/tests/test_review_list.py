from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from review_app.models import Review
from rest_framework import status


User = get_user_model()


class ReviewFilterTests(APITestCase):

    def setUp(self):
        self.review_author = User.objects.create_user(
            username="review_author",
            password="Testpassword123!",
            type="customer",
        )

        self.reviewed_business_user = User.objects.create_user(
            username="first_business_user",
            password="Testpassword123!",
            type="business",
        )

        self.other_business_user = User.objects.create_user(
            username="second_business_user",
            password="Testpassword123!",
            type="business",
        )

        self.expected_review = Review.objects.create(
            reviewer=self.review_author,
            business_user=self.reviewed_business_user,
            rating=5,
            description="Expected review",
        )

        Review.objects.create(
            reviewer=self.review_author,
            business_user=self.other_business_user,
            rating=3,
            description="Other review",
        )


    def test_only_reviews_for_selected_business_user_are_returned(self):
        response = self.client.get(
            f"/api/reviews/?business_user_id="
            f"{self.reviewed_business_user.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        returned_review = response.data[0]

        self.assertEqual(returned_review["id"], self.expected_review.id)
        self.assertEqual(returned_review["business_user"], self.reviewed_business_user.id)


    def test_only_reviews_from_selected_author_are_returned(self):
        other_review_author = User.objects.create_user(
            username="other_review_author",
            password="Testpassword123!",
            type="customer",
        )

        Review.objects.create(
            reviewer=other_review_author,
            business_user=self.reviewed_business_user,
            rating=2,
            description="Review from another author",
        )

        response = self.client.get(
            f"/api/reviews/?reviewer_id="f"{self.review_author.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        for returned_review in response.data:
            self.assertEqual(
                returned_review["reviewer"],
                self.review_author.id,
            )



    def test_reviews_are_sorted_by_highest_rating(self):
        response = self.client.get("/api/reviews/?ordering=-rating")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        first_review = response.data[0]
        second_review = response.data[1]
        self.assertEqual(first_review["rating"],5)
        self.assertEqual(second_review["rating"], 3)
