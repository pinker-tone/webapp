# Generated by Django 2.2 on 2019-04-11 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'verbose_name': 'Game', 'verbose_name_plural': 'Games'},
        ),
        migrations.AlterModelOptions(
            name='questions',
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
    ]
