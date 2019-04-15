# Generated by Django 2.2 on 2019-04-15 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('battle', '0010_auto_20190414_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='answers_correct_user_1',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='answers_correct_user_2',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='draw',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='winner', to=settings.AUTH_USER_MODEL, verbose_name='Winner'),
        ),
        migrations.DeleteModel(
            name='GameHistory',
        ),
    ]
