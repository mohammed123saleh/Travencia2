# Generated by Django 2.2.15 on 2021-05-26 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0043_auto_20210526_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='Number_OF_Guests',
            field=models.CharField(choices=[('one', 1), ('two', 2), ('three', 3), ('four', 4), ('five', 5), ('six', 6), ('seven', 7), ('eight', 8), ('nine', 9), ('ten', 10), ('eleven', 11), ('tweleve', 12), ('thirteen', 13), ('fourteen', 14), ('fifteen', 15), ('sixteen', 16), ('seventeen', 17), ('eighteen', 18), ('nineteen', 19), ('twenty', 20)], max_length=10),
        ),
    ]