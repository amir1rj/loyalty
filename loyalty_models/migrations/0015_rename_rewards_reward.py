# Generated by Django 5.1.2 on 2024-10-15 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_models', '0014_rename_tiers_tier'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rewards',
            new_name='Reward',
        ),
    ]
