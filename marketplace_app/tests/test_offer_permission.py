from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from marketplace_app.models import MarketplaceOffer

User = get_user_model()

class OfferPermissionTests(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer_user",
            password="Testpassword123!",
            type="customer",
        )

        self.offer_data = {
            "title": "Testangebot",
            "description": "Testdedescription",
            "details": [
                {
                    "title": "Basic",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": "100.00",
                    "features": ["Testfunktion"],
                    "offer_type": "basic",
                }
            ],
        }

    def test_customer_can_not_create_offer(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post("/api/offers/", self.offer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MarketplaceOffer.objects.count(),0)