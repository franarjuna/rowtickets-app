from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_paymentmethod_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='display_name',
            field=models.CharField(max_length=255, verbose_name='Nombre para mostrar'),
        ),
    ]
