from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)

class Menu(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField()

class Tables(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    url = models.CharField()
    
class Reservation(models.Model):
    account_id = models.ForeignKey(Account)
    menu_id = models.ForeignKey(Menu)
    table_id = models.ForeignKey(Tables , null=True)
    created_at = models.DateTimeField(auto_created=True)

class Stroage(models.Model):
    title = models.CharField
    remined_material = models.IntegerField()
    expire_date = models.DateField()
    
    