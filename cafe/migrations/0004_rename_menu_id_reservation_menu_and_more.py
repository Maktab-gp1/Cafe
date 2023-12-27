# Generated by Django 5.0 on 2023-12-27 16:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cafe", "0003_menu_category_reservation_is_confirmed_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reservation", old_name="menu_id", new_name="menu",
        ),
        migrations.RenameField(
            model_name="reservation", old_name="table_id", new_name="table",
        ),
        migrations.AddField(
            model_name="menu", name="number", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="reservation",
            name="reserved_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="menu", name="category", field=models.CharField(max_length=150),
        ),
    ]