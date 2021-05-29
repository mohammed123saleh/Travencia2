# Generated by Django 3.1 on 2020-10-15 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0008_auto_20201012_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='show',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Hotel Name'),
        ),
    ]