# Generated by Django 2.2.15 on 2021-04-12 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0021_order_customer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Customer_Name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
