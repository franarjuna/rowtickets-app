from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='billing_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_billing_address', to='addresses.address', verbose_name='Dirección de envío'),
        ),
        migrations.AddField(
            model_name='user',
            name='shipping_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_shipping_address', to='addresses.address', verbose_name='Dirección de facturación'),
        ),
    ]
