# Generated by Django 5.1.1 on 2024-10-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flo', '0009_fueltransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='init_fuel',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]