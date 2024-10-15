# Generated by Django 5.1.2 on 2024-10-15 05:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_models', '0005_pointrole_priority_alter_pointrole_point_role_type_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalservice',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='AdditionalServices', to=settings.AUTH_USER_MODEL),
        ),
    ]
