# Generated by Django 3.1 on 2020-08-27 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_details_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='details',
            name='title',
        ),
    ]