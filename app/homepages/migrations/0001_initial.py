from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homepage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, unique=True, verbose_name='país')),
            ],
            options={
                'verbose_name': 'página principal',
                'verbose_name_plural': 'páginas principales',
            },
        ),
        migrations.CreateModel(
            name='HomepageSlide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('image', models.ImageField(height_field='image_height', upload_to='event_gallery_images', verbose_name='imagen', width_field='image_width')),
                ('image_width', models.PositiveIntegerField(blank=True, null=True, verbose_name='ancho')),
                ('image_height', models.PositiveIntegerField(blank=True, null=True, verbose_name='alto')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homepage_slides', to='events.event', verbose_name='evento')),
                ('homepage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepages.homepage', related_name='slides')),
            ],
            options={
                'verbose_name': 'slide',
                'verbose_name_plural': 'slides',
                'ordering': ('homepage', 'order'),
            },
        )
    ]
