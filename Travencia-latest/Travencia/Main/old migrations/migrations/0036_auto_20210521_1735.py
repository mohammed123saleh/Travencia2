# Generated by Django 2.2.15 on 2021-05-21 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0035_auto_20210521_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='Terms',
            field=models.BooleanField(default=False),
        ),
    ]
