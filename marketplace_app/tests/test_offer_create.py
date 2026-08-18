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
            "title": "Neue Website",
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