# Generated by Django 3.2.3 on 2021-12-21 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_userbookrelation_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=12, max_digits=7),
            preserve_default=False,
        ),
    ]
