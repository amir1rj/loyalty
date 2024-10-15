# Generated by Django 5.1.2 on 2024-10-15 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_models', '0009_rename_points_userpoints_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointrole',
            name='rewards',
        ),
        migrations.AddField(
            model_name='pointrole',
            name='reward',
            field=models.ManyToManyField(blank=True, related_name='point_roles', to='loyalty_models.rewards'),
        ),
    ]
