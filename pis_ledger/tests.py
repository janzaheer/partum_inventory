import pytest
from django.urls import reverse

from pis_ledger.models import Ledger
from pis_ledger.forms import LedgerForm
from tests.factories import (
    RetailerUserFactory, RetailerFactory, CustomerFactory,
    LedgerFactory,
)

pytestmark = pytest.mark.django_db


class TestLedgerModel:
    def test_create(self):
        ledger = LedgerFactory()
        assert ledger.pk is not None

    def test_str(self):
        customer = CustomerFactory(customer_name='John Doe')
        ledger = LedgerFactory(customer=customer)
        assert str(ledger) == 'John Doe'

    def test_timestamps(self):
        ledger = LedgerFactory()
        assert ledger.created_at is not None
        assert ledger.updated_at is not None

    def test_defaults(self):
        customer = CustomerFactory()
        ledger = Ledger.objects.create(customer=customer)
        assert ledger.amount == 0
        assert ledger.payment == 0
        assert ledger.person == 'customer'


class TestLedgerForm:
    def test_valid(self):
        retailer = RetailerFactory()
        customer = CustomerFactory(retailer=retailer)
        form = LedgerForm(data={
            'retailer': retailer.id,
            'customer': customer.id,
            'amount': 500.00,
            'payment': 200.00,
            'description': 'Test ledger entry',
        })
        assert form.is_valid()

    def test_invalid_missing_customer(self):
        form = LedgerForm(data={'amount': 500.00})
        assert not form.is_valid()


class TestLedgerViews:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_customer_ledger_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('ledger:customer_ledger_list'))
        assert response.status_code == 200

    def test_customer_ledger_detail(self, client):
        client.login(username=self.user.username, password='testpass123')
        customer = CustomerFactory(retailer=self.retailer_user.retailer)
        LedgerFactory(retailer=self.retailer_user.retailer, customer=customer, amount=1000, payment=500)
        response = client.get(
            reverse('ledger:customer_ledger_detail', kwargs={'customer_id': customer.pk}))
        assert response.status_code == 200

    def test_add_ledger(self, client):
        client.login(username=self.user.username, password='testpass123')
        customer = CustomerFactory(retailer=self.retailer_user.retailer)
        response = client.get(
            reverse('ledger:add_ledger', kwargs={'customer_id': customer.pk}))
        assert response.status_code == 200

    def test_add_payment(self, client):
        client.login(username=self.user.username, password='testpass123')
        customer = CustomerFactory(retailer=self.retailer_user.retailer)
        response = client.get(
            reverse('ledger:add_payment', kwargs={'customer_id': customer.pk}))
        assert response.status_code == 200

    def test_unauthenticated_redirects(self, client):
        response = client.get(reverse('ledger:customer_ledger_list'))
        assert response.status_code == 302

    def test_create_ledger_view(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('ledger:add_new_ledger'))
        assert response.status_code == 200
