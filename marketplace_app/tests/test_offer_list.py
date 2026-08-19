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
            title="Testoffer",
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
        self.assertEqual(offer["title"], "Testoffer")
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


    def test_filter_offers_by_creator(self):
        other_business_user = User.objects.create_user(
            username="other_business_user",
            password="Testpassword123!",
            type="business",
        )

        MarketplaceOffer.objects.create(
            user=other_business_user,
            title="The other offer from other user",
            description="Testdescription",
        )

        response = self.client.get(f"/api/offers/?creator_id={self.business_user.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"],1)
        found_offer = response.data["results"][0]
        self.assertEqual(found_offer["user"], self.business_user.id)


    def test_filter_offers_max_delivery_time(self):
        offer_with_long_delivery_time = MarketplaceOffer.objects.create(
            user=self.business_user,
            title="Offer that takes longer",
            description="Delivery is longer",
        )

        OfferPackage.objects.create(
            offer=offer_with_long_delivery_time,
            title="Slow Basic",
            revisions=1,
            delivery_time_in_days=10,
            price="400.00",
            features=["Testoffer"],
            offer_type="basic",
        )

        response = self.client.get("/api/offers/?max_delivery_time=3")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"],1)
        found_offer = response.data["results"][0]
        self.assertEqual(found_offer["title"], "Testoffer")
        self.assertEqual(found_offer["min_delivery_time"],3)


    def test_order_offers_min_price(self):
        expensive_offer = MarketplaceOffer.objects.create(
            user=self.business_user,
            title="expensives offer",
            description="This offer is expensiv.",
        )

        OfferPackage.objects.create(
            offer=expensive_offer,
            title="Expensive Basic",
            revisions=1,
            delivery_time_in_days=5,
            price="400.00",
            features=["Testfunktion"],
            offer_type="basic",
        )

        response = self.client.get("/api/offers/?ordering=min_price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"],2)
        first_offer = response.data["results"][0]
        second_offer = response.data["results"][1]
        self.assertEqual(first_offer["min_price"], "55.00")
        self.assertEqual(second_offer["min_price"], "400.00")