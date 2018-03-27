from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from pis_com.models import DatedModel


class Retailer(DatedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=False)

    def __unicode__(self):
        return self.name


class RetailerUser(models.Model):
    user = models.OneToOneField(User, related_name='retailer_user')
    retailer = models.ForeignKey(Retailer, related_name='u_retailer')

