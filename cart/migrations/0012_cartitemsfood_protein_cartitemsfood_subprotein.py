# Generated by Django 4.2.3 on 2024-07-04 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_cart_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitemsfood',
            name='protein',
            field=models.CharField(default='beef', max_length=30),
        ),
        migrations.AddField(
            model_name='cartitemsfood',
            name='subprotein',
            field=models.CharField(default='fried beef', max_length=30),
        ),
    ]
