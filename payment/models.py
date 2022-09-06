from django.db import models


class Order(models.Model):
    braintree_id = models.CharField(max_length=150, blank=True)
