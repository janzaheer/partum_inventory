import pytest
from django.urls import reverse
from django.contrib.auth.models import User

from pis_com.models import FeedBack, UserProfile, DatedModel
from pis_com.forms import CustomerForm, FeedBackForm
from tests.factories import (
    RetailerFactory, RetailerUserFactory,
    CustomerFactory, FeedBackFactory, AdminConfigurationFactory,
)

pytestmark = pytest.mark.django_db


class TestDatedModel:
    def test_abstract_model(self):
        assert DatedModel._meta.abstract is True


class TestAdminConfiguration:
    def test_create(self):
        config = AdminConfigurationFactory()
        assert config.production is False
        assert config.demo is False
        assert config.local is True

    def test_str(self):
        config = AdminConfigurationFactory()
        assert 'AdminConfiguration' in str(config)


class TestUserProfile:
    def test_auto_created_on_user_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        assert hasattr(user, 'user_profile')
        assert user.user_profile.user_type == UserProfile.USER_TYPE_SHOP

    def test_str(self):
        user = User.objects.create_user(username='profileuser', password='testpass123')
        assert str(user.user_profile) == 'profileuser'

    def test_not_duplicated(self):
        user = User.objects.create_user(username='uniqueuser', password='testpass123')
        assert UserProfile.objects.filter(user=user).count() == 1
        user.save()
        assert UserProfile.objects.filter(user=user).count() == 1


class TestCustomerModel:
    def test_create(self):
        customer = CustomerFactory()
        assert customer.pk is not None
        assert 'Customer' in customer.customer_name

    def test_str(self):
        customer = CustomerFactory(customer_name='Test Customer')
        assert str(customer) == 'Test Customer'

    def test_default_type(self):
        customer = CustomerFactory()
        assert customer.customer_type == 'customer'


class TestFeedBackModel:
    def test_create(self):
        feedback = FeedBackFactory()
        assert feedback.pk is not None

    def test_str(self):
        feedback = FeedBackFactory(description='Great service!')
        assert str(feedback) == 'Great service!'

    def test_str_with_none(self):
        feedback = FeedBackFactory(description=None)
        assert str(feedback) == ''

    def test_date_auto_set(self):
        feedback = FeedBackFactory()
        assert feedback.date is not None


class TestCustomerForm:
    def test_valid(self):
        retailer = RetailerFactory()
        form = CustomerForm(data={
            'retailer': retailer.id,
            'customer_name': 'Test Customer',
            'customer_phone': '03001234567',
        })
        assert form.is_valid()

    def test_invalid_missing_name(self):
        retailer = RetailerFactory()
        form = CustomerForm(data={'retailer': retailer.id})
        assert not form.is_valid()
        assert 'customer_name' in form.errors


class TestFeedBackForm:
    def test_valid(self):
        retailer = RetailerFactory()
        form = FeedBackForm(data={
            'retailer': retailer.id,
            'description': 'Nice product',
        })
        assert form.is_valid()


class TestLoginView:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_page_loads(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_success(self, client):
        response = client.post(reverse('login'), {
            'username': self.user.username,
            'password': 'testpass123',
        })
        assert response.status_code == 302

    def test_failure(self, client):
        response = client.post(reverse('login'), {
            'username': self.user.username,
            'password': 'wrongpassword',
        })
        assert response.status_code == 200

    def test_authenticated_user_redirected(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('login'))
        assert response.status_code == 302


class TestLogoutView:
    def test_redirects(self, client):
        ru = RetailerUserFactory()
        client.login(username=ru.user.username, password='testpass123')
        response = client.get(reverse('logout'))
        assert response.status_code == 302


class TestHomePageView:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_unauthenticated_redirected(self, client):
        response = client.get(reverse('index'))
        assert response.status_code == 302

    def test_authenticated_owner_sees_homepage(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('index'))
        assert response.status_code == 200


class TestCustomerView:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_list_view(self, client):
        client.login(username=self.user.username, password='testpass123')
        CustomerFactory(retailer=self.retailer_user.retailer)
        response = client.get(reverse('customers'))
        assert response.status_code == 200

    def test_unauthenticated_redirects(self, client):
        response = client.get(reverse('customers'))
        assert response.status_code == 302


class TestFeedBackView:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_page_loads(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('create_feedback'))
        assert response.status_code == 200

    def test_submit(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.post(reverse('create_feedback'), {
            'retailer': self.retailer_user.retailer.id,
            'description': 'Great app!',
        })
        assert response.status_code == 302
        assert FeedBack.objects.filter(description='Great app!').exists()


class TestReportsView:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_unauthenticated_redirects(self, client):
        response = client.get(reverse('reports'))
        assert response.status_code == 302

    def test_authenticated_sees_reports(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('reports'))
        assert response.status_code == 200
