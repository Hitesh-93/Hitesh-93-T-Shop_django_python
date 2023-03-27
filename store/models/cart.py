from django.db import models
from django.contrib.auth.models import User
from .size import SizeVarient





class Cart(models.Model):
    sizeVarient = models.ForeignKey(SizeVarient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

