import pytest
from django.urls import reverse

from pis_retailer.models import RetailerUser
from pis_retailer.forms import RetailerForm, RetailerUserForm
from tests.factories import RetailerFactory, RetailerUserFactory, UserFactory, ProductFactory

pytestmark = pytest.mark.django_db


class TestRetailerModel:
    def test_create(self):
        retailer = RetailerFactory()
        assert retailer.pk is not None
        assert 'Retailer' in retailer.name

    def test_str(self):
        retailer = RetailerFactory(name='My Shop')
        assert str(retailer) == 'My Shop'

    def test_timestamps(self):
        retailer = RetailerFactory()
        assert retailer.created_at is not None
        assert retailer.updated_at is not None


class TestRetailerUserModel:
    def test_create(self):
        retailer_user = RetailerUserFactory()
        assert retailer_user.pk is not None
        assert retailer_user.role_type == RetailerUser.ROLE_TYPE_OWNER

    def test_str(self):
        retailer_user = RetailerUserFactory()
        assert str(retailer_user) == retailer_user.user.username

    def test_role_types(self):
        assert RetailerUser.ROLE_TYPE_OWNER == 'owner'
        assert RetailerUser.ROLE_TYPE_DATA_ENTRY_USER == 'data_entry_user'
        assert RetailerUser.ROLE_TYPE_SALESMAN == 'salesman'
        assert RetailerUser.ROLE_TYPE_VIEW_ACCOUNT == 'account_viewer'
        assert RetailerUser.ROLE_TYPE_LEDGER_VIEW == 'ledger_viewer'


class TestRetailerForm:
    def test_valid(self):
        form = RetailerForm(data={'name': 'Test Retailer', 'slug': 'test-retailer'})
        assert form.is_valid()

    def test_invalid_missing_slug(self):
        form = RetailerForm(data={'name': 'Test Retailer'})
        assert not form.is_valid()
        assert 'slug' in form.errors


class TestRetailerUserForm:
    def test_valid(self):
        user = UserFactory()
        retailer = RetailerFactory()
        form = RetailerUserForm(data={
            'user': user.id,
            'retailer': retailer.id,
            'role_type': RetailerUser.ROLE_TYPE_OWNER,
        })
        assert form.is_valid()


class TestRetailerProductsAPI:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_unauthenticated_redirects(self, client):
        response = client.get(
            reverse('retailer:retailer_products',
                    kwargs={'retailer_id': self.retailer_user.retailer.pk}))
        assert response.status_code == 302

    def test_authenticated_returns_json(self, client):
        client.login(username=self.user.username, password='testpass123')
        ProductFactory(retailer=self.retailer_user.retailer)
        response = client.get(
            reverse('retailer:retailer_products',
                    kwargs={'retailer_id': self.retailer_user.retailer.pk}))
        assert response.status_code == 200
        data = response.json()
        assert 'retailer_products' in data
        assert len(data['retailer_products']) == 1
