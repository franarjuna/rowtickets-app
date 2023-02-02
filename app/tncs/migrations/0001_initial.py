from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TnC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('country', models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile')], db_index=True, max_length=2, verbose_name='país')),
                ('title', models.CharField(max_length=150, verbose_name='título')),
                ('content', django_quill.fields.QuillField(verbose_name='contenido')),
                ('order', models.PositiveIntegerField(db_index=True, default=0)),
            ],
            options={
                'verbose_name': 'término',
                'verbose_name_plural': 'términos y condiciones',
                'ordering': ('country', 'order'),
                'unique_together': {('country', 'order')},
            },
        ),
    ]
