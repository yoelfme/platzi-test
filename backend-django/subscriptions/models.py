from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible, smart_text

@python_2_unicode_compatible
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    payment_date = models.DateTimeField(null=True)
    stripe_id = models.CharField(max_length=25, null=True)
    stripe_subscription_id = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return smart_text("{0} - {1}".format(self.name, self.email))
