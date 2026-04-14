from django.db import models


class ExtraExpense(models.Model):
    amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.amount) if self.amount is not None else ''
