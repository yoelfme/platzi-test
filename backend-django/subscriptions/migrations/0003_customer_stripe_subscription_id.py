# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_auto_20161015_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='stripe_subscription_id',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
    ]
