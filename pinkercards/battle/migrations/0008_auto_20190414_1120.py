# Generated by Django 2.2 on 2019-04-14 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0007_auto_20190414_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamehistory',
            name='answers_correct_user_2',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
