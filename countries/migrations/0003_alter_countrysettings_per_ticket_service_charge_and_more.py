# Generated by Django 4.1.4 on 2023-06-23 02:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0002_alter_countrysettings_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrysettings',
            name='per_ticket_service_charge',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='service charge'),
        ),
        migrations.AlterField(
            model_name='countrysettings',
            name='ticket_price_surcharge_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='cargo plataforma (porcentaje sobre precio vendedor)'),
        ),
    ]
