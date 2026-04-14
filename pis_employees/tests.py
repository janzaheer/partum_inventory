import pytest
from django.urls import reverse

from pis_employees.models import Employee
from pis_employees.forms import EmployeeForm, EmployeeSalaryForm
from tests.factories import (
    RetailerUserFactory, EmployeeFactory, EmployeeSalaryFactory,
)

pytestmark = pytest.mark.django_db


class TestEmployeeModel:
    def test_create(self):
        employee = EmployeeFactory()
        assert employee.pk is not None

    def test_str(self):
        employee = EmployeeFactory(cnic='12345-6789012-1')
        assert str(employee) == '12345-6789012-1'

    def test_str_with_none(self):
        employee = EmployeeFactory(cnic=None)
        assert str(employee) == ''


class TestEmployeeSalaryModel:
    def test_create(self):
        salary = EmployeeSalaryFactory()
        assert salary.pk is not None

    def test_str(self):
        employee = EmployeeFactory(cnic='CNIC-001')
        salary = EmployeeSalaryFactory(employee=employee)
        assert str(salary) == 'CNIC-001'

    def test_str_with_no_employee(self):
        salary = EmployeeSalaryFactory(employee=None)
        assert str(salary) == ''


class TestEmployeeForm:
    def test_valid(self):
        form = EmployeeForm(data={
            'name': 'John Doe',
            'father_name': 'Richard Doe',
            'cnic': '12345-6789012-1',
            'mobile': '03001234567',
            'address': '123 Main St',
            'date_of_joining': '2024-01-01',
        })
        assert form.is_valid()

    def test_allows_blank(self):
        form = EmployeeForm(data={})
        assert form.is_valid()


class TestEmployeeSalaryForm:
    def test_valid(self):
        employee = EmployeeFactory()
        form = EmployeeSalaryForm(data={
            'employee': employee.id,
            'salary_amount': '50000',
            'date': '2024-01-31',
        })
        assert form.is_valid()


class TestEmployeeViews:
    def setup_method(self):
        self.retailer_user = RetailerUserFactory()
        self.user = self.retailer_user.user

    def test_list(self, client):
        client.login(username=self.user.username, password='testpass123')
        EmployeeFactory()
        response = client.get(reverse('employee:employee_list'))
        assert response.status_code == 200

    def test_add(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.get(reverse('employee:add_new_employee'))
        assert response.status_code == 200

    def test_add_post(self, client):
        client.login(username=self.user.username, password='testpass123')
        response = client.post(reverse('employee:add_new_employee'), {
            'name': 'Jane Smith',
            'cnic': '99999-1234567-1',
            'mobile': '03009876543',
        })
        assert response.status_code == 302
        assert Employee.objects.filter(name='Jane Smith').exists()

    def test_delete(self, client):
        client.login(username=self.user.username, password='testpass123')
        employee = EmployeeFactory()
        response = client.post(
            reverse('employee:delete_employee', kwargs={'pk': employee.pk}))
        assert response.status_code == 302
        assert not Employee.objects.filter(pk=employee.pk).exists()

    def test_salary_detail(self, client):
        client.login(username=self.user.username, password='testpass123')
        employee = EmployeeFactory()
        EmployeeSalaryFactory(employee=employee)
        response = client.get(
            reverse('employee:employee_salary_detail', kwargs={'pk': employee.pk}))
        assert response.status_code == 200

    def test_unauthenticated_redirects(self, client):
        response = client.get(reverse('employee:add_new_employee'))
        assert response.status_code == 302
