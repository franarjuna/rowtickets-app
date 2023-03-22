from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0008_section_ticket_remove_eventticket_event_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, verbose_name='país')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='comprador')),
            ],
            options={
                'verbose_name': 'compra',
                'verbose_name_plural': 'compras',
            },
        ),
        migrations.CreateModel(
            name='OrderTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('quantity', models.PositiveIntegerField(verbose_name='cantidad')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_tickets', to='orders.order', verbose_name='compra')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_tickets', to='events.ticket', verbose_name='ticket')),
            ],
            options={
                'verbose_name': 'ticket de compra',
                'verbose_name_plural': 'tickets de compra',
            },
        ),
    ]
