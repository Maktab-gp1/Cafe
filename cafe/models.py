from django.db import models
from django.urls import reverse


class Account(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Tables(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    url = models.CharField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Reservation(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    menu = models.ManyToManyField(Menu)
    table = models.ForeignKey(Tables, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_created=True)
    is_confirmed = models.BooleanField(default=False)
    reserved_time = models.DateTimeField()
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
