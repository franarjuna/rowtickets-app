from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, verbose_name='país')),
                ('question', models.CharField(max_length=255, verbose_name='pregunta')),
                ('answer', django_quill.fields.QuillField(blank=True, verbose_name='respuesta')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
            ],
            options={
                'verbose_name': 'pregunta frecuente',
                'verbose_name_plural': 'preguntas frecuentes',
                'ordering': ('country', 'order'),
                'unique_together': {('country', 'order')},
            },
        ),
    ]
