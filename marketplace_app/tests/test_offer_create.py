from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from marketplace_app.models import MarketplaceOffer, OfferPackage

User = get_user_model()

class CreateMarketplaceOfferTests(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            password="Testpassword123!",
            type="business",
        )
        self.client.force_authenticate(
           user=self.business_user,
        )

    def test_business_user_can_create_offer(self):
        new_offer_data = {
            "title": "New Website",
            "description": "Ich erstelle eine Website.",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": "100.00",
                    "features": ["Testfunktion"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": "200.00",
                    "features": ["Testfunktion"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium",
                    "revisions": 3,
                    "delivery_time_in_days": 7,
                    "price": "300.00",
                    "features": ["Testfunktion"],
                    "offer_type": "premium",
                },
            ],
        }

        response = self.client.post("/api/offers/",new_offer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,)
        self.assertEqual(MarketplaceOffer.objects.count(),1)
        created_offer = MarketplaceOffer.objects.first()
        self.assertEqual(created_offer.user, self.business_user)
        self.assertEqual(created_offer.title,"New Website")
        self.assertEqual(OfferPackage.objects.filter(offer=created_offer).count(),3)

    def test_offer_can_not_be_created_with_less_than_three_packages(self):
        new_offer_data = {
            "title": "Incomplete offer",
            "description": "This offer has only one package.",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": "100.00",
                    "features": ["Test feature"],
                    "offer_type": "basic",
                },
            ],
        }

        response = self.client.post("/api/offers/", new_offer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MarketplaceOffer.objects.count(), 0)

    def test_offer_requires_basic_standard_and_premium_packages(self):
        package_data = {
            "title": "Basic",
            "revisions": 1,
            "delivery_time_in_days": 3,
            "price": "100.00",
            "features": ["Test feature"],
            "offer_type": "basic",
        }
        new_offer_data = {
            "title": "Offer with duplicate package types",
            "description": "This offer contains three basic packages.",
            "details": [package_data, package_data, package_data],
        }

        response = self.client.post("/api/offers/", new_offer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(MarketplaceOffer.objects.count(), 0)
