# Generated by Django 4.2.3 on 2023-12-19 05:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_app', '0015_alter_soup_medium_box_name_alter_soup_mega_box_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soup',
            name='image',
            field=models.ImageField(upload_to='media', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])]),
        ),
    ]
