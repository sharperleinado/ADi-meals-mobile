# Generated by Django 4.2.3 on 2024-07-26 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_remove_useraddress_area_remove_useraddress_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='division',
            field=models.CharField(max_length=50, null=True),
        ),
    ]