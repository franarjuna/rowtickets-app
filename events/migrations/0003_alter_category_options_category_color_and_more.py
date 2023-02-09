from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_options_category_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('country', 'order'), 'verbose_name': 'categoría', 'verbose_name_plural': 'categorías'},
        ),
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(choices=[('blue', 'Azul'), ('green', 'Verde'), ('pink', 'Rosa'), ('red', 'Rojo'), ('orange', 'Naranja')], default='pink', max_length=20, verbose_name='color'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='header_image',
            field=models.ImageField(default='', height_field='header_image_height', upload_to='category_header_images', verbose_name='imagen de cabecera', width_field='header_image_width'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='header_image_height',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='alto de imagen de cabecera'),
        ),
        migrations.AddField(
            model_name='category',
            name='header_image_width',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='ancho de imagen de cabecera'),
        ),
    ]
