# Generated by Django 2.2.15 on 2021-04-13 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0024_auto_20210413_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Deposit',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='Email',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='Guests_Number',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='Hotel_Name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='Hotel_Rate',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='Nights',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='Rest',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='Tax',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='Tel',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='Total',
            field=models.CharField(max_length=250),
        ),
    ]
