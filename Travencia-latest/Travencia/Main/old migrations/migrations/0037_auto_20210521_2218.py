# Generated by Django 2.2.15 on 2021-05-21 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0036_auto_20210521_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='promo_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
