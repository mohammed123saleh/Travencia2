# Generated by Django 2.2.15 on 2021-05-26 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0042_auto_20210526_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='item',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.Item'),
        ),
    ]
