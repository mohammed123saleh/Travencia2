# Generated by Django 2.2.15 on 2021-04-12 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0019_auto_20210413_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='CVC',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='Card_Holder',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='Card_Number',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='Expires',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='Terms',
            field=models.CharField(max_length=50),
        ),
    ]