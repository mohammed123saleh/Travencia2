# Generated by Django 2.2.15 on 2021-05-26 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0038_auto_20210526_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='details',
            field=models.ManyToManyField(editable=False, to='Main.Details'),
        ),
    ]
