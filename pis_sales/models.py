import random

from django.db import models
from django.db.models.signals import post_save

from pis_com.models import DatedModel


class SalesHistory(DatedModel):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer', related_name='retailer_sales', on_delete=models.CASCADE
    )
    receipt_no = models.CharField(
        max_length=20, unique=True, blank=True, null=True, db_index=True
    )
    customer = models.ForeignKey(
        'pis_com.Customer',
        related_name='customer_sales',
        blank=True, null=True, on_delete=models.CASCADE
    )
    product_details = models.TextField(
        max_length=512, blank=True, null=True,
        help_text='Quantity and Product name would save in JSON format')
    purchased_items = models.ManyToManyField(
        'pis_product.PurchasedProduct', blank=True
    )
    extra_items = models.ManyToManyField(
        'pis_product.ExtraItems', blank=True,
    )
    total_quantity = models.DecimalField(
        max_digits=65, decimal_places=2, default=1, blank=True, null=True)
    sub_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    paid_amount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    remaining_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    discount = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    shipping = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    grand_total = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    cash_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )
    returned_payment = models.DecimalField(
        max_digits=65, decimal_places=2, default=0, blank=True, null=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Sales histories'
        indexes = [
            models.Index(fields=['retailer', 'created_at'], name='sales_retailer_created_idx'),
        ]

    def __str__(self):
        return self.retailer.name


def create_save_receipt_no(sender, instance, created, **kwargs):
    if created and not instance.receipt_no:
        while True:
            random_code = random.randint(1000000, 9999999)
            if not SalesHistory.objects.filter(receipt_no=random_code).exists():
                break

        instance.receipt_no = random_code
        instance.save()


post_save.connect(create_save_receipt_no, sender=SalesHistory)
