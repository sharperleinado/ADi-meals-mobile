# Generated by Django 4.2.3 on 2024-07-18 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_transactions_boxsize'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='datetime',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
