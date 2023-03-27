from django.db import models
from django.contrib.auth.models import User
from .tshirt import Tshirt
from .size import SizeVarient




class Order(models.Model):
    orderStatus = (
        ('PENDING', "Pending"),
        ('PLACED', "Placed"),
        ('CANCELED', "Canceled"),
        ('COMPLETED', "Completed")
    )
    
    payMethods = (
        ('COD', "Cash on delivery"),
        ('ONLINE', "Online"),
    )

    order_status = models.CharField(max_length=15, choices = orderStatus)
    payment_method = models.CharField(max_length=15, choices = payMethods)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)
    shipping_address = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=10, null=False)





class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tshirt = models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVarient, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)