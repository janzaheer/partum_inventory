# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-08-07 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pis_ledger', '0007_auto_20190807_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='ledger',
            name='dated',
            field=models.DateField(blank=True, null=True),
        ),
    ]
