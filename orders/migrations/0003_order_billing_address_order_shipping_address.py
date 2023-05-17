from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
        ('orders', '0002_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_billing_address', to='addresses.address', verbose_name='Dirección de facturación'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_shipping_address', to='addresses.address', verbose_name='Dirección de envío'),
        ),
    ]
