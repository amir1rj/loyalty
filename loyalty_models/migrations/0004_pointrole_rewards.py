# Generated by Django 5.1.2 on 2024-10-14 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_models', '0003_rename_awards_rewards_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointrole',
            name='rewards',
            field=models.ManyToManyField(blank=True, null=True, to='loyalty_models.rewards'),
        ),
    ]
