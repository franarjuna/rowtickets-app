import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountrySettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, unique=True, verbose_name='país')),
                ('per_ticket_service_charge', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='cargo de servicio por entrada')),
                ('ticket_price_surcharge_percentage', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='porcentaje de recargo al precio base')),
            ],
            options={
                'verbose_name': 'configuración de país',
                'verbose_name_plural': 'configuraciones de país',
            },
        ),
    ]
