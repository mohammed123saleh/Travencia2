# Generated by Django 2.2.15 on 2021-05-26 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0045_auto_20210527_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='Number_OF_Guests',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20)], default=1, max_length=10),
        ),
    ]
