from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from marketplace_app.models import MarketplaceOffer, OfferPackage
from order_app.models import Order

User = get_user_model()

class OrderCountTests(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            password="Testpassword123!",
            type="business",
        )

        self.customer_user = User.objects.create_user(
            username="customer_user",
            password="Testpassword123!",
            type="customer",
        )

        offer = MarketplaceOffer.objects.create(
            user=self.business_user,
            title="Testangebot",
            description="Testbeschreibung",
        )

        package = OfferPackage.objects.create(
            offer=offer,
            title="Basic",
            revisions=1,
            delivery_time_in_days=3,
            price="100.00",
            features=["Testfunktion"],
            offer_type="basic",
        )

        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer_detail=package,
            title=package.title,
            revisions=package.revisions,
            delivery_time_in_days=package.delivery_time_in_days,
            price=package.price,
            features=package.features,
            offer_type=package.offer_type,
            status="in_progress",
        )

        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer_detail=package,
            title=package.title,
            revisions=package.revisions,
            delivery_time_in_days=package.delivery_time_in_days,
            price=package.price,
            features=package.features,
            offer_type=package.offer_type,
            status="completed",
        )

    def test_count_open_orders(self):
        self.client.force_authenticate(user=self.business_user)

        response = self.client.get( f"/api/order-count/{self.business_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"],1)


    def test_count_finished_orders(self):
        self.client.force_authenticate(user=self.business_user)

        response = self.client.get(f"/api/completed-order-count/"f"{self.business_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"], 1,)