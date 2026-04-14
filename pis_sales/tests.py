import pytest
from decimal import Decimal
from django.urls import reverse

from pis_sales.models import SalesHistory
from pis_sales.forms import BillingForm
from tests.factories import (
    RetailerUserFactory, RetailerFactory, SalesHistoryFactory,
    ProductFactory, StockInFactory,
)

pytestmark = pytest.mark.django_db


class TestSalesHistoryModel:
    def test_create(self):
        sale = SalesHistoryFactory()
        assert sale.pk is not None
        assert sale.receipt_no is not None

    def test_str(self):
        retailer = RetailerFactory(name='Test Shop')
        sale = SalesHistoryFactory(retailer=retailer)
        assert str(sale) == 'Test Shop'

    def test_receipt_no_auto_generated(self):
        retailer = RetailerFactory()
        sale = SalesHistory.objects.create(retailer=retailer, grand_total=100)
        assert sale.receipt_no is not None

    def test_unique_receipt_numbers(self):
        retailer = RetailerFactory()
        sale1 = SalesHistoryFactory(retailer=retailer)
        sale2 = SalesHistoryFactory(retailer=retailer)
        assert sale1.receipt_no != sale2.receipt_no

    def test_timestamps(self):
        sale = SalesHistoryFactory()
        assert sale.created_at is not None
        assert sale.updated_at is not None


class TestBillingForm:
    def test_valid(self):
        retailer = RetailerFactory()
        form = BillingForm(data={
            'retailer': retailer.id,
            'grand_total': 500.00,
            'paid_amount': 500.00,
            'remaining_payment': 0,
            'discount': 0,
            'total_quantity': '5',
        })
        assert form.is_valid()


class TestInvoiceViews:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_create_invoice_view(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('sales:create_invoice'))
        assert response.status_code == 200

    def test_invoice_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        SalesHistoryFactory(retailer=self.retailer_user.retailer)
        response = client.get(reverse('sales:invoice_list'))
        assert response.status_code == 200

    def test_invoice_detail(self, client):
        client.login(username=self.user.username, password='testpass123')
        sale = SalesHistoryFactory(retailer=self.retailer_user.retailer)
        response = client.get(
            reverse('sales:invoice_detail', kwargs={'invoice_id': sale.pk}))
        assert response.status_code == 200

    def test_unauthenticated_redirects(self, client):
        response = client.get(reverse('sales:create_invoice'))
        assert response.status_code == 302

    def test_product_items_api(self, client):
        client.login(username=self.user.username, password='testpass123')
        product = ProductFactory(retailer=self.retailer_user.retailer)
        StockInFactory(product=product, quantity=Decimal('100'))
        response = client.get(reverse('sales:product_item_api'))
        assert response.status_code == 200
        data = response.json()
        assert 'products' in data

    def test_delete_invoice(self, client):
        client.login(username=self.user.username, password='testpass123')
        sale = SalesHistoryFactory(retailer=self.retailer_user.retailer)
        response = client.post(
            reverse('sales:delete', kwargs={'pk': sale.pk}))
        assert response.status_code == 302
        assert not SalesHistory.objects.filter(pk=sale.pk).exists()


class TestReportAPIs:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_daily_sales_api(self, client):
        client.login(username=self.user.username, password='testpass123')
        SalesHistoryFactory(retailer=self.retailer_user.retailer)
        response = client.get(reverse('api_sales_daily'))
        assert response.status_code == 200
        data = response.json()
        assert 'sales_data' in data
        assert len(data['sales_data']) == 7

    def test_weekly_sales_api(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('api_sales_weekly'))
        assert response.status_code == 200
        data = response.json()
        assert 'sales_data' in data
        assert len(data['sales_data']) == 4

    def test_monthly_sales_api(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('api_sales_monthly'))
        assert response.status_code == 200
        data = response.json()
        assert 'sales_data' in data
        assert len(data['sales_data']) > 0

    def test_unauthenticated_redirects(self, client):
        response = client.get(reverse('api_sales_daily'))
        assert response.status_code == 302
