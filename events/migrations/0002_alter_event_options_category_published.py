from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-date',), 'verbose_name': 'evento', 'verbose_name_plural': 'eventos'},
        ),
        migrations.AddField(
            model_name='category',
            name='published',
            field=models.BooleanField(default=True, verbose_name='publicada'),
        ),
    ]
