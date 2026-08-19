from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from marketplace_app.models import MarketplaceOffer, OfferPackage
from order_app.models import Order

User = get_user_model()

class OrderUpdateTests(APITestCase):

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
            title="Testoffer",
            description="Testdescription",
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

    def test_business_user_can_updates_order_status(self):
        self.client.force_authenticate(user=self.business_user)

        update_data = {"status": "completed"}
        response = self.client.patch(f"/api/orders/{self.order.id}/", update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")


    def test_other_business_user_can_not_update_other_order(self):
        other_business_user = User.objects.create_user(
            username="other_business_user",
            password="Testpassword123!",
            type="business",
        )

        self.client.force_authenticate(user=other_business_user)

        update_data = {"status": "completed"}
        response = self.client.patch(f"/api/orders/{self.order.id}/", update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "in_progress")


    def test_customer_can_not_update_order_business_user_status(self):
        self.client.force_authenticate(user=self.customer_user)

        update_data = {"status": "completed"}
        response = self.client.patch(f"/api/orders/{self.order.id}/", update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "in_progress")


    def test_invalid_order_status_is_dismiss(self):
        self.client.force_authenticate(user=self.business_user)

        update_data = {"status": "defer"}
        response = self.client.patch(f"/api/orders/{self.order.id}/", update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status,"in_progress")