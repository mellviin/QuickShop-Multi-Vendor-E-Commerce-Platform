from django.db import models
from django.contrib.auth.models import User
from quickshop.products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("placed", "Order Placed"),
        ("packed", "Packed"),
        ("shipped", "Shipped"),
        ("delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    address = models.TextField()
    city = models.CharField(max_length=100)

    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="placed")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"