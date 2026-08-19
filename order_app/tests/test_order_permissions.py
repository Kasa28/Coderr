from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from marketplace_app.models import MarketplaceOffer, OfferPackage
from order_app.models import Order

User = get_user_model()

class OrderPermissionTests(APITestCase):

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

        self.other_customer = User.objects.create_user(
            username="other_customer",
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

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer_detail=package,
            title=package.title,
            revisions=package.revisions,
            delivery_time_in_days=package.delivery_time_in_days,
            price=package.price,
            features=package.features,
            offer_type=package.offer_type,
        )

    def test_other_customer_can_not_view_order(self):
        self.client.force_authenticate(user=self.other_customer)

        response = self.client.get(f"/api/orders/{self.order.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)