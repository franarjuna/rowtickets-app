from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_category_options_category_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(choices=[('blue', 'Azul'), ('green', 'Verde'), ('orange', 'Naranja'), ('pink', 'Rosa'), ('red', 'Rojo')], max_length=20, verbose_name='color'),
        ),
    ]
