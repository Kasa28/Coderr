from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from marketplace_app.models import MarketplaceOffer, OfferPackage

User = get_user_model()

class OfferDetailTests(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            password="Testpassword123!",
            type="business",
        )

        self.offer = MarketplaceOffer.objects.create(
            user=self.business_user,
            title="Testangebot",
            description="Testdescription",
        )

        OfferPackage.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=1,
            delivery_time_in_days=3,
            price="100.00",
            features=["Testfunktion"],
            offer_type="basic",
        )

    def test_get_single_offer(self):
        response = self.client.get(f"/api/offers/{self.offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"],self.offer.id)
        self.assertEqual(response.data["title"],"Testangebot")
        self.assertEqual(len(response.data["details"]),1)