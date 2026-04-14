import pytest
from decimal import Decimal
from django.urls import reverse

from pis_expense.models import ExtraExpense
from pis_expense.forms import ExtraExpenseForm
from tests.factories import RetailerUserFactory, ExtraExpenseFactory

pytestmark = pytest.mark.django_db


class TestExtraExpenseModel:
    def test_create(self):
        expense = ExtraExpenseFactory()
        assert expense.pk is not None

    def test_str(self):
        expense = ExtraExpenseFactory(amount=Decimal('1500'))
        assert str(expense) == '1500'

    def test_str_with_none(self):
        expense = ExtraExpenseFactory(amount=None)
        assert str(expense) == ''


class TestExtraExpenseForm:
    def test_valid(self):
        form = ExtraExpenseForm(data={
            'amount': '500',
            'description': 'Office supplies',
            'date': '2024-01-15',
        })
        assert form.is_valid()

    def test_allows_blank(self):
        form = ExtraExpenseForm(data={})
        assert form.is_valid()


class TestExpenseViews:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        ExtraExpenseFactory()
        response = client.get(reverse('expense:expense_list'))
        assert response.status_code == 200

    def test_add(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('expense:add_new_expense'))
        assert response.status_code == 200

    def test_add_post(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.post(reverse('expense:add_new_expense'), {
            'amount': '1000',
            'description': 'Electricity bill',
            'date': '2024-01-20',
        })
        assert response.status_code == 302
        assert ExtraExpense.objects.filter(amount=Decimal('1000')).exists()

    def test_delete(self, client):
        client.login(username=self.user.username, password='testpass123')
        expense = ExtraExpenseFactory()
        response = client.post(
            reverse('expense:delete_expense', kwargs={'pk': expense.pk}))
        assert response.status_code == 302
        assert not ExtraExpense.objects.filter(pk=expense.pk).exists()

    def test_unauthenticated_redirects(self, client):
        response = client.get(reverse('expense:add_new_expense'))
        assert response.status_code == 302
