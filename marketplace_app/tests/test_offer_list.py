from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from marketplace_app.models import (MarketplaceOffer, OfferPackage)

User = get_user_model()

class GetMarketplaceOfferListTests(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            password="Testpassword123!",
            type="business",
        )
        self.offer = MarketplaceOffer.objects.create(
            user=self.business_user,
            title="Testangebot",
            description="Test.",
        )
        OfferPackage.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=1,
            delivery_time_in_days=3,
            price="100.00",
            features=["Eine Seite"],
            offer_type="basic",
        )

    def test_get_offer_list(self):
        response = self.client.get("/api/offers/")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        offer = response.data["results"][0]
        self.assertEqual(offer["title"], "Testangebot")
        self.assertEqual(offer["user"], self.business_user.id)
        self.assertEqual(offer["min_price"], "100.00")
        self.assertEqual(offer["min_delivery_time"], 3)
        self.assertEqual(len(offer["details"]), 1)


    def test_search_offer_by_title(self):
        MarketplaceOffer.objects.create(
            user=self.business_user,
            title="Search Title",
            description="Description",
        )

        response = self.client.get("/api/offers/?search=Search")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"],1)

        found_offer = response.data["results"][0]

        self.assertEqual(found_offer["title"],"Search Title")