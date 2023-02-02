from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='about_us_module_button_text',
            field=models.CharField(default='Conocenos', max_length=150, verbose_name='módulo quienes somos: texto botón'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_us_module_heading',
            field=models.CharField(default='Nosotros y nuestros partners', max_length=150, verbose_name='módulo quienes somos: encabezado'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_us_module_subtitle',
            field=models.CharField(default='Somos un grupo de profesionales a tu servicio.', max_length=150, verbose_name='módulo quienes somos: subtítulo'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_us_module_text',
            field=models.TextField(default='RowTicket es la plataforma de compra y venta secundaria de entradas. Con entradas disponibles para eventos deportivos, musicales y de teatro, en todo Latam.', verbose_name='módulo quienes somos: texto'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_us_module_title',
            field=models.CharField(default='Más de 20 años de experiencia', max_length=150, verbose_name='módulo quienes somos: título'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='contact_us_module_event_today',
            field=models.CharField(default='¿El evento es hoy?', max_length=100, verbose_name='módulo contacto: ¿el evento es hoy?'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='contact_us_module_text',
            field=models.TextField(default='Por consultas o ventas coorporativas contactate con nosotros', verbose_name='módulo contacto: texto'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='sell_module_button_text',
            field=models.CharField(default='Vender entradas', max_length=80, verbose_name='módulo vender: texto botón'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='sell_module_text',
            field=models.TextField(default='Establece el precio y ajústalo en cualquier momento antes de que se vendan tus entradas. La entrega es rápida y sin complicaciones seguida del pago puntual. Manejamos las comunicaciones con los compradores.', verbose_name='módulo vender: texto'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='sell_module_title',
            field=models.CharField(default='Vende con tranquilidad', max_length=150, verbose_name='módulo vender: título'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='warranty_module_buy_sell_text',
            field=models.CharField(default='Compra y vende con confianza', max_length=150, verbose_name='módulo garantía: texto compra venta'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='warranty_module_customer_service_text',
            field=models.CharField(default='Servicio al cliente hasta su asiento', max_length=150, verbose_name='módulo garantía: texto servicio al cliente'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='warranty_module_warranty_text',
            field=models.CharField(default='Cada pedido está 100% garantizado', max_length=150, verbose_name='módulo garantía: texto garantía'),
        ),
    ]
