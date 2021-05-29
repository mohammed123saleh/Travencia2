# Generated by Django 2.2.15 on 2021-03-16 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0011_item_mo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveField(
            model_name='item',
            name='mo',
        ),
        migrations.AlterField(
            model_name='item',
            name='convention_image',
            field=models.ImageField(default='Hotel/moha.jpeg', upload_to='Hotel'),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, help_text='random input', max_length=500, null=True),
        ),
    ]
