from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from marketplace_app.models import MarketplaceOffer, OfferPackage
from order_app.models import Order
from decimal import Decimal

User = get_user_model()

class OrderCreationTests(APITestCase):

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

        self.offer = MarketplaceOffer.objects.create(
            user=self.business_user,
            title="Testoffer",
            description="Testdescription",
        )

        self.offer_package = OfferPackage.objects.create(
            offer=self.offer,
            title="Basic",
            revisions=1,
            delivery_time_in_days=3,
            price="100.00",
            features=["Testfunktion"],
            offer_type="basic",
        )

    def test_customer_create_order(self):
        self.client.force_authenticate(user=self.customer_user)
        order_data = {"offer_detail_id": self.offer_package.id}
        response = self.client.post("/api/orders/", order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        created_order = Order.objects.first()

        self.assertEqual(created_order.customer_user, self.customer_user)
        self.assertEqual(created_order.business_user, self.business_user)
        self.assertEqual(created_order.offer_detail, self.offer_package)
        self.assertEqual(created_order.price, Decimal("100.00"))
        self.assertEqual(created_order.status,"in_progress")


    def test_business_user_can_not_create_order(self):
        self.client.force_authenticate(
            user=self.business_user,
        )

        order_data = {"offer_detail_id": self.offer_package.id}
        response = self.client.post("/api/orders/", order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Order.objects.count(), 0)


    def test_invalid_offer_detail_id_can_not_create_order(self):
        self.client.force_authenticate(user=self.customer_user)
        order_data = {"offer_detail_id": 99999}
        response = self.client.post("/api/orders/", order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Order.objects.count(), 0)
