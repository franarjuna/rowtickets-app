from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in_progress', 'En proceso'), ('pending_payment_confirmation', 'Esperando confirmación de pago'), ('paid', 'Paga'), ('cancelled', 'Cancelada')], default='cancelled', max_length=50, verbose_name='estado'),
            preserve_default=False,
        ),
    ]
