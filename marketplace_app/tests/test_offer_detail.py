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
            title="Testoffer",
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
        self.assertEqual(response.data["title"],"Testoffer")
        self.assertEqual(len(response.data["details"]),1)


    def test_owner_can_update_offer_title(self):
        self.client.force_authenticate(user=self.business_user)
        update_data = {"title": "Change offer title"}
        response = self.client.patch(f"/api/offers/{self.offer.id}/",update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.title, "Change offer title")


    def test_other_user_can_not_update_offer(self):
        other_business_user = User.objects.create_user(
            username="other_business_user",
            password="Testpassword123!",
            type="business",
        )

        self.client.force_authenticate(user=other_business_user)
        update_data = {"title": "external changes"}
        response = self.client.patch(f"/api/offers/{self.offer.id}/", update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.title,"Testoffer")

    def test_owner_can_delete_offer(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.delete(f"/api/offers/{self.offer.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MarketplaceOffer.objects.count(),0)
        self.assertEqual(OfferPackage.objects.count(),0)