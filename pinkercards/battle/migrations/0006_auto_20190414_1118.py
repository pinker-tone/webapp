# Generated by Django 2.2 on 2019-04-14 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0005_auto_20190413_1604'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamehistory',
            options={'verbose_name': 'Game History', 'verbose_name_plural': 'Games History'},
        ),
        migrations.AlterField(
            model_name='gamehistory',
            name='winner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='winner', to=settings.AUTH_USER_MODEL, verbose_name='Winner'),
        ),
    ]
