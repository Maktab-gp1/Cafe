# Generated by Django 5.0.1 on 2024-01-17 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_cafe_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
