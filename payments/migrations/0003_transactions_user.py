# Generated by Django 4.2.3 on 2024-07-17 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0002_alter_transactions_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]