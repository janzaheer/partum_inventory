from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone



class DatedModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AdminConfiguration(models.Model):
    production = models.BooleanField(default=False)
    demo = models.BooleanField(default=False)
    local = models.BooleanField(default=False)


class UserProfile(models.Model):
    USER_TYPE_SHOP = 'shop'
    USER_TYPE_COMPANY = 'company'
    USER_TYPE_INDIVIDUAL = 'individual'

    USER_TYPES = (
        (USER_TYPE_SHOP, 'Shop'),
        (USER_TYPE_COMPANY, 'Company'),
        (USER_TYPE_INDIVIDUAL, 'Individual'),
    )

    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=100, choices=USER_TYPES, default=USER_TYPE_SHOP
    )
    address = models.TextField(max_length=512, blank=True, null=True)
    phone_no = models.CharField(max_length=13, blank=True, null=True)
    mobile_no = models.CharField(max_length=13, blank=True, null=True)
    picture = models.ImageField(
        upload_to='images/profile/picture/', max_length=1024, blank=True
    )
    date_of_birth = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class Customer(models.Model):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer',
        related_name='retailer_customer',
        on_delete=models.CASCADE
    )
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_type=models.CharField(max_length=200, default='customer', blank=True, null=True)
    address = models.TextField(max_length=500, blank=True,null=True)
    shop = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.customer_name


class FeedBack(models.Model):
    retailer = models.ForeignKey(
        'pis_retailer.Retailer',
        related_name='retailer_feedback', null=True, blank=True,
        on_delete=models.CASCADE
    )
    description= models.CharField(max_length=200, null=True, blank=True)
    date=date=models.DateField(default=timezone.now, null=True, blank=True)

    def __unicode__(self):
        return self.description

# Signal Functions
def create_profile(sender, instance, created, **kwargs):
    """
    The functions used to check if user profile is not created
    and created the user profile without saving role and hospital
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created and not UserProfile.objects.filter(user=instance):
        return UserProfile.objects.create(
            user=instance
        )


# Signals
post_save.connect(create_profile, sender=User)
