import pytest
from decimal import Decimal
from django.urls import reverse

from pis_supplier.models import Supplier
from pis_supplier.forms import SupplierForm, SupplierStatementForm
from tests.factories import (
    RetailerUserFactory, SupplierFactory, SupplierStatementFactory,
)

pytestmark = pytest.mark.django_db


class TestSupplierModel:
    def test_create(self):
        supplier = SupplierFactory()
        assert supplier.pk is not None

    def test_str(self):
        supplier = SupplierFactory(name='ABC Supplies')
        assert str(supplier) == 'ABC Supplies'

    def test_str_with_none(self):
        supplier = SupplierFactory(name=None)
        assert str(supplier) == ''

    def test_remaining_amount(self):
        supplier = SupplierFactory()
        SupplierStatementFactory(supplier=supplier, supplier_amount=Decimal('10000'), payment_amount=Decimal('3000'))
        SupplierStatementFactory(supplier=supplier, supplier_amount=Decimal('5000'), payment_amount=Decimal('2000'))
        assert supplier.supplier_remaining_amount() == Decimal('10000')


class TestSupplierStatementModel:
    def test_create(self):
        statement = SupplierStatementFactory()
        assert statement.pk is not None

    def test_str(self):
        supplier = SupplierFactory(name='XYZ Corp')
        statement = SupplierStatementFactory(supplier=supplier)
        assert str(statement) == 'XYZ Corp'

    def test_str_with_no_supplier(self):
        statement = SupplierStatementFactory(supplier=None)
        assert str(statement) == ''

    def test_remaining_amount(self):
        statement = SupplierStatementFactory(supplier_amount=Decimal('10000'), payment_amount=Decimal('6000'))
        assert statement.remaining_amount() == Decimal('4000')


class TestSupplierForm:
    def test_valid(self):
        form = SupplierForm(data={
            'name': 'Test Supplier',
            'address': '123 Supply St',
            'phone': '021-1234567',
            'mobile_no': '03001234567',
        })
        assert form.is_valid()

    def test_allows_blank(self):
        form = SupplierForm(data={})
        assert form.is_valid()


class TestSupplierStatementForm:
    def test_valid(self):
        supplier = SupplierFactory()
        form = SupplierStatementForm(data={
            'supplier': supplier.id,
            'supplier_amount': 10000,
            'payment_amount': 5000,
            'description': 'Monthly payment',
            'date': '2024-01-15',
        })
        assert form.is_valid()


class TestSupplierViews:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('supplier:list_supplier'))
        assert response.status_code == 200

    def test_add(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('supplier:add_supplier'))
        assert response.status_code == 200

    def test_add_post(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.post(reverse('supplier:add_supplier'), {
            'name': 'New Supplier',
            'address': '456 Trade Ave',
            'phone': '021-9876543',
        })
        assert response.status_code == 302
        assert Supplier.objects.filter(name='New Supplier').exists()

    def test_statement_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        supplier = SupplierFactory()
        SupplierStatementFactory(supplier=supplier)
        response = client.get(
            reverse('supplier:list_supplier_statement', kwargs={'pk': supplier.pk}))
        assert response.status_code == 200

    def test_add_statement(self, client):
        client.login(username=self.user.username, password='testpass123')
        supplier = SupplierFactory()
        response = client.get(
            reverse('supplier:add_supplier_statement', kwargs={'pk': supplier.pk}))
        assert response.status_code == 200

    def test_unauthenticated_redirects(self, client):
        response = client.get(reverse('supplier:list_supplier'))
        assert response.status_code == 302

    def test_statement_payment(self, client):
        client.login(username=self.user.username, password='testpass123')
        supplier = SupplierFactory()
        response = client.get(
            reverse('supplier:payment', kwargs={'pk': supplier.pk}))
        assert response.status_code == 200
