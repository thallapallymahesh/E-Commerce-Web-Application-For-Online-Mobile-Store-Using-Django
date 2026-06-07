from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    CATEGORY_CHOICES = (
        ('Samsung', 'Samsung'),
        ('Apple', 'Apple'),
        ('Vivo', 'Vivo'),
        ('Oppo', 'Oppo'),
        ('OnePlus', 'OnePlus'),
        ('Redmi', 'Redmi'),
        ('IQOO', 'IQOO'),
    )

    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)

    def get_total(self):
        total = 0

        for item in self.orderitem_set.all():
            total += item.product.price * item.quantity

        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name