# Generated by Django 2.2.15 on 2021-04-12 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0020_auto_20210413_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Customer_Name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
