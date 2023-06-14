from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mercadopago_payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mercadopagopaymentmethod',
            options={'verbose_name': 'Método de pago Mercado Pago', 'verbose_name_plural': 'Métodos de pago Mercado Pago'},
        ),
    ]
