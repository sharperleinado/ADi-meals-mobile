# Generated by Django 4.1.6 on 2023-07-13 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_delete_cartitemssoup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitemsfood',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]