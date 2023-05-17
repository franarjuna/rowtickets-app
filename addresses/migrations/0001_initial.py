from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('address_type', models.CharField(choices=[('billing', 'Facturación'), ('shipping', 'Envío')], max_length=50, verbose_name='tipo de dirección')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Nombre')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='Apellido')),
                ('company_name', models.CharField(blank=True, max_length=255, verbose_name='Nombre de la empresa (opcional)')),
                ('street_address_1', models.CharField(blank=True, max_length=255, verbose_name='Dirección (línea 1)')),
                ('street_address_2', models.CharField(blank=True, max_length=255, verbose_name='Dirección (línea 2)')),
                ('city', models.CharField(blank=True, max_length=255, verbose_name='Ciudad / Localidad')),
                ('country_area', models.CharField(blank=True, max_length=255, verbose_name='Estado / Provincia / Región')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, verbose_name='país')),
                ('postal_code', models.CharField(blank=True, max_length=64, verbose_name='Código postal')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=30, verbose_name='Email')),
                ('iva_status', models.CharField(blank=True, choices=[('consumidor_final', 'Consumidor Final'), ('responsable_inscripto', 'Responsable Inscripto')], max_length=30, verbose_name='Condición frente al IVA')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Dirección',
                'verbose_name_plural': 'Direcciones',
                'ordering': ('-created',),
            },
        ),
    ]
