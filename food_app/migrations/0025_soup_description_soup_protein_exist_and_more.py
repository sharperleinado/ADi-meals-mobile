# Generated by Django 4.2.3 on 2025-01-19 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_app', '0024_food_description_food_protein_exist'),
    ]

    operations = [
        migrations.AddField(
            model_name='soup',
            name='description',
            field=models.CharField(default='one complimentary tin milk', max_length=1000),
        ),
        migrations.AddField(
            model_name='soup',
            name='protein_exist',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='yes', max_length=30),
        ),
        migrations.AlterField(
            model_name='food',
            name='description',
            field=models.CharField(default='one complimentary tin milk', max_length=1000),
        ),
        migrations.AlterField(
            model_name='food',
            name='protein_exist',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='yes', max_length=30),
        ),
    ]
