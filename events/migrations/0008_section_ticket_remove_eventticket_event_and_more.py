import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0007_rename_eventplaces_eventplace_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('name', models.CharField(max_length=150, verbose_name='nombre')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, verbose_name='color')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='events.event', verbose_name='evento')),
            ],
            options={
                'verbose_name': 'sectores del evento',
                'verbose_name_plural': 'sectores del evento',
                'ordering': ('event', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='precio final')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='precio')),
                ('ticket_type', models.CharField(choices=[('paper', 'Papel'), ('e_ticket', 'E Ticket'), ('electronic_ticket_transfer', 'Transferencia de entradas electrónicas')], max_length=50, verbose_name='tipo de entrada')),
                ('ready_to_ship', models.BooleanField(verbose_name='listo para enviar')),
                ('extra_info', models.CharField(blank=True, max_length=255, verbose_name='información extra')),
                ('quantity', models.PositiveIntegerField(verbose_name='cantidad')),
                ('selling_condition', models.CharField(choices=[('no_preference', 'Sin preferencia'), ('sold_together', 'Se venden juntas'), ('no_single_ticket_unsold', 'No dejar 1 sin vender'), ('sold_by_pairs', 'Se venden de a pares')], default='no_preference', max_length=50, verbose_name='condición de venta')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='events.event', verbose_name='evento')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.section', verbose_name='sector')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to=settings.AUTH_USER_MODEL, verbose_name='vendedor')),
            ],
            options={
                'verbose_name': 'entradas',
                'verbose_name_plural': 'entradas',
                'ordering': ('event', 'price'),
            },
        ),
        migrations.RemoveField(
            model_name='eventticket',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventticket',
            name='user',
        ),
        migrations.DeleteModel(
            name='EventPlace',
        ),
        migrations.DeleteModel(
            name='EventTicket',
        ),
    ]
