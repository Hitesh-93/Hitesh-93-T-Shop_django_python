from django.db import models
from django.contrib.auth.models import User
from .order import Order





class Payment(models.Model):
    date = models.DateTimeField(null=False, auto_now_add=True)
    payment_status = models.CharField(max_length=15, default="FAILED")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=60)
    payment_request_id = models.CharField(max_length=60, unique=True, null=False)
