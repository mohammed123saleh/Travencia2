# Generated by Django 2.2.15 on 2021-04-18 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0027_auto_20210413_0500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Csv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='csv files')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Da',
        ),
    ]
