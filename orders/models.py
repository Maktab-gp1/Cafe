from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from shop.models import Product

# Create your models here.
class Table(models.Model):
    id = models.IntegerField(unique = True, primary_key=True )
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"Table No. {self.id}"


class Order(models.Model):
    class Status(models.TextChoices):
        PROCESS = "PR",_("Process")
        CONFIRMED = "CF",_("Confirmed")
        PAYED = "PA",_("Paid")

    phone = models.CharField(unique=True, max_length=12)
    table = models.ForeignKey(Table,on_delete=models.SET_NULL ,null = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,choices = Status,
        db_default=Status.PROCESS,
        )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_absolute_url(self): 
        return reverse('orderstaffupdate',
                      args=[self.pk])


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
