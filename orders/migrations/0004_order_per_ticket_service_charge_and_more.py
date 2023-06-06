import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_billing_address_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='per_ticket_service_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='cargo de servicio por entrada'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='service_charge_subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='subtotal por cargo de servicio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='ticket_price_surcharge_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='porcentaje de recargo al precio base'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='tickets_subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='subtotal de tickets'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='total'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderticket',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='precio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderticket',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='precio final'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderticket',
            name='service_charge_subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='subtotal por cargo de servicio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderticket',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='subtotal'),
            preserve_default=False,
        ),
    ]
