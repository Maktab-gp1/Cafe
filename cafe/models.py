from django.db import models
from django.urls import reverse



class Account(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)

    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length= 150)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title

class Tables(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    url = models.CharField()

    def __str__(self) -> str:
        return self.name


class Reservation(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    menu_id = models.ManyToManyField(Menu)
    table_id = models.ForeignKey(Tables, on_delete=models.SET_NULL , null = True)
    created_at = models.DateTimeField(auto_created=True)
    is_confirmed = models.BooleanField(default=False)
    # slug = models.SlugField(unique=True, null=True, blank=True)

    # def get_absolute_url(self):
    #     return reverse("book_detail", kwargs={"slug": self.slug})
    # def __str__(self) -> str:
    #     return self.id


class Storage(models.Model):
    material_title = models.CharField()
    remined_material = models.IntegerField()
    expire_date = models.DateField()

    def __str__(self) -> str:
        return self.material_title

