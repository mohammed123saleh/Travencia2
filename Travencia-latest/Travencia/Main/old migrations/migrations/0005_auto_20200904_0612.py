# Generated by Django 3.1 on 2020-09-04 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_item_convention_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(help_text='random input', max_length=500),
        ),
    ]
