from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    cnic = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    date_of_joining = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-date_of_joining']

    def __str__(self):
        return self.cnic or ''


class EmployeeSalary(models.Model):
    employee = models.ForeignKey(
        Employee, related_name='employee_salary',
        null=True, blank=True, on_delete=models.CASCADE)
    salary_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Employee salaries'

    def __str__(self):
        return str(self.employee) if self.employee else ''
