# Generated by Django 5.0 on 2023-12-19 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='table_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe.tables'),
        ),
    ]
