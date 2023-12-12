from django.db import models
from moneyfield import MoneyField
# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)


class Menu(models.Model):
    title = models.CharField(max_length=100)
    price = models.MoneyField(
        decimal_places=2, max_digits=8, currency_default='Rial')
    description = models.TextField()


class Tables(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    url = models.CharField()


class Reservation(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    table_id = models.ForeignKey(Tables, null=True)
    created_at = models.DateTimeField(auto_created=True)


class Storage(models.Model):
    material_title = models.CharField()
    remined_material = models.IntegerField()
    expire_date = models.DateField()
