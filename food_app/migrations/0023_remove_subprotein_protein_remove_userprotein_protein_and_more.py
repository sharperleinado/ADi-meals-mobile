# Generated by Django 4.2.3 on 2024-07-04 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food_app', '0022_remove_food_protein_remove_food_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subprotein',
            name='protein',
        ),
        migrations.RemoveField(
            model_name='userprotein',
            name='protein',
        ),
        migrations.RemoveField(
            model_name='userprotein',
            name='subprotein',
        ),
        migrations.RemoveField(
            model_name='userprotein',
            name='user',
        ),
        migrations.DeleteModel(
            name='Protein',
        ),
        migrations.DeleteModel(
            name='SubProtein',
        ),
        migrations.DeleteModel(
            name='UserProtein',
        ),
    ]