from django.db import models
from django.urls import reverse



class Account(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)


class Menu(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()


class Tables(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    url = models.CharField()


class Reservation(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)


    table_id = models.ForeignKey(Tables, on_delete=models.SET_NULL , null = True)

    created_at = models.DateTimeField(auto_created=True)
    # slug = models.SlugField(unique=True, null=True, blank=True)

    # def get_absolute_url(self):
    #     return reverse("book_detail", kwargs={"slug": self.slug})


class Storage(models.Model):
    material_title = models.CharField()
    remined_material = models.IntegerField()
    expire_date = models.DateField()
