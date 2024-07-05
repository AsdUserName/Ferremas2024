from unittest.mock import MagicMock, patch

from api.models import Product
from api.serializers import ProductSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class ViewsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("api.views.ProductSerializer")
    def test_product_create(self, mock_product_serializer):
        # Mock the ProductSerializer
        mock_product_serializer.return_value.is_valid.return_value = True
        mock_product_serializer.return_value.save.return_value = Product(
            id=1, name="New Product", price=100.0, stock=10
        )

        url = reverse("product-create")
        data = {"name": "New Product", "price": 100.0, "stock": 10}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Product")

    @patch("api.views.Transaction")
    def test_webpay_plus_create(self, mock_transaction):
        # Mock the Transaction.create() method
        mock_transaction.return_value.create.return_value = {
            "token": "mock_token",
            "url": "http://mock-url.com",
        }

        url = reverse("webpay-plus-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("request", response.data)
        self.assertIn("response", response.data)
        self.assertIn("url_webpay_form", response.data)

    @patch("api.views.Transaction")
    def test_commit_webpay_transaction(self, mock_transaction):
        # Mock the Transaction.commit() method
        mock_transaction.return_value.commit.return_value = {
            "status": "success",
            "detail": "Transaction committed",
        }

        url = reverse("webpay-plus-commit") + "?token_ws=mock_token"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Success")
        self.assertEqual(response.data["detail"]["status"], "success")
        self.assertEqual(response.data["detail"]["detail"], "Transaction committed")
