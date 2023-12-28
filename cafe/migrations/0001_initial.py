# Generated by Django 5.0 on 2023-12-28 07:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('category', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_title', models.CharField(max_length=100)),
                ('remined_material', models.IntegerField()),
                ('expire_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('url', models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('reserved_time', models.DateTimeField()),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.account')),
                ('menu', models.ManyToManyField(to='cafe.menu')),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe.tables')),
            ],
        ),
    ]
