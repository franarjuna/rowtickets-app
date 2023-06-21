from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_remove_address_iva_status_alter_address_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='ar_dni',
            field=models.CharField(blank=True, max_length=100, verbose_name='DNI'),
        ),
        migrations.AddField(
            model_name='address',
            name='ar_iva_condition',
            field=models.CharField(blank=True, choices=[('consumidor_final', 'Consumidor Final'), ('responsable_inscripto', 'Responsable Inscripto')], max_length=100, verbose_name='Condición frente al IVA'),
        ),
        migrations.AddField(
            model_name='address',
            name='cl_rut',
            field=models.CharField(blank=True, max_length=100, verbose_name='RUT'),
        ),
    ]
