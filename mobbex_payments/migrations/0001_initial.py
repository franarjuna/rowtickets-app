from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0004_merge_20230606_1201'),
        ('orders', '0005_merge_20230606_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobbexPaymentMethod',
            fields=[
                ('paymentmethod_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.paymentmethod')),
                ('api_key', models.CharField(max_length=255, verbose_name='API Key')),
                ('access_token', models.CharField(max_length=255, verbose_name='Access token')),
                ('test_mode', models.BooleanField(verbose_name='modo test')),
            ],
            options={
                'verbose_name': 'Método de pago Mobbex',
                'verbose_name_plural': 'Métodos de pago Mobbex',
            },
            bases=('payments.paymentmethod',),
        ),
        migrations.CreateModel(
            name='MobbexPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('request_data', models.JSONField(verbose_name='data (request)')),
                ('response_data', models.JSONField(verbose_name='data (response)')),
                ('checkout_id', models.CharField(blank=True, db_index=True, max_length=255, unique=True, verbose_name='checkout ID')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mobbex_payments', to='orders.order', verbose_name='compra')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mobbex_payments', to='mobbex_payments.mobbexpaymentmethod', verbose_name='medio de pago')),
            ],
            options={
                'verbose_name': 'Pago Mobbex',
                'verbose_name_plural': 'Pagos Mobbex',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='MobbexIPN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('data', models.JSONField(verbose_name='data (request)')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ipns', to='mobbex_payments.mobbexpayment', verbose_name='Pago Mobbex')),
            ],
            options={
                'verbose_name': 'IPN Mobbex',
                'verbose_name_plural': 'IPNs Mobbex',
                'ordering': ('-created',),
            },
        ),
    ]
