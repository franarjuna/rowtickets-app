from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, verbose_name='país')),
                ('slug', models.SlugField(max_length=80, verbose_name='nombre en URL')),
                ('name', models.CharField(max_length=150, verbose_name='nombre')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
            ],
            options={
                'verbose_name': 'categoría',
                'verbose_name_plural': 'categorías',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, verbose_name='país')),
                ('slug', models.SlugField(max_length=80, verbose_name='nombre en URL')),
                ('title', models.CharField(max_length=150, verbose_name='nombre')),
                ('date', models.DateTimeField(db_index=True, verbose_name='fecha y hora')),
                ('date_text', models.CharField(blank=True, max_length=150, verbose_name='fecha (texto)')),
                ('online_event', models.BooleanField(default=False, verbose_name='evento online')),
                ('highlighted', models.BooleanField(default=False, verbose_name='destacado')),
                ('published', models.BooleanField(default=False, verbose_name='publicado')),
                ('main_image', models.ImageField(height_field='main_image_height', upload_to='event_main_images', verbose_name='imagen principal', width_field='main_image_width')),
                ('main_image_width', models.PositiveIntegerField(blank=True, null=True, verbose_name='ancho de imagen principal')),
                ('main_image_height', models.PositiveIntegerField(blank=True, null=True, verbose_name='alto de imagen principal')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='events', to='events.category', verbose_name='categoría')),
            ],
            options={
                'verbose_name': 'evento',
                'verbose_name_plural': 'eventos',
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, verbose_name='país')),
                ('slug', models.SlugField(max_length=80, verbose_name='nombre en URL')),
                ('name', models.CharField(max_length=150, verbose_name='nombre')),
                ('twitter_handle', models.CharField(blank=True, max_length=150, verbose_name='usuario de Twitter')),
            ],
            options={
                'verbose_name': 'organizador',
                'verbose_name_plural': 'organizadores',
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, verbose_name='país')),
                ('slug', models.SlugField(max_length=80, verbose_name='nombre en URL')),
                ('name', models.CharField(max_length=150, verbose_name='nombre')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='dirección')),
            ],
            options={
                'verbose_name': 'sede',
                'verbose_name_plural': 'sedes',
            },
        ),
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('image', models.ImageField(height_field='image_height', upload_to='event_images', verbose_name='imagen', width_field='image_width')),
                ('image_width', models.PositiveIntegerField(blank=True, null=True, verbose_name='ancho')),
                ('image_height', models.PositiveIntegerField(blank=True, null=True, verbose_name='alto')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_images', to='events.event', verbose_name='evento')),
            ],
            options={
                'verbose_name': 'imagen de evento',
                'verbose_name_plural': 'imágenes de evento',
                'ordering': ('event', 'order'),
            },
        ),
        migrations.CreateModel(
            name='EventGalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('image', models.ImageField(height_field='image_height', upload_to='event_gallery_images', verbose_name='imagen', width_field='image_width')),
                ('image_width', models.PositiveIntegerField(blank=True, null=True, verbose_name='ancho')),
                ('image_height', models.PositiveIntegerField(blank=True, null=True, verbose_name='alto')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_gallery_images', to='events.event', verbose_name='evento')),
            ],
            options={
                'verbose_name': 'imagen de galería de evento',
                'verbose_name_plural': 'imágenes de galería de evento',
                'ordering': ('event', 'order'),
            },
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='events', to='events.venue', verbose_name='sede'),
        ),
    ]
