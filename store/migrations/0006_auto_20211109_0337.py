# Generated by Django 3.2.3 on 2021-11-09 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0005_auto_20211108_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='readers',
            field=models.ManyToManyField(related_name='books', through='store.UserBookRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userbookrelation',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.book', unique=True),
        ),
    ]