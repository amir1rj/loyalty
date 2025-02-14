# Generated by Django 5.1.2 on 2024-10-14 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_models', '0002_pointrolegroup_pointrole_point_role_type_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Awards',
            new_name='Rewards',
        ),
        migrations.AlterField(
            model_name='pointrole',
            name='point_role_type',
            field=models.CharField(choices=[('number_of_purchases', 'Number of Classrooms'), ('number_of_purchases_with_specific_classroom', 'Number of Classrooms with Specific Classroom'), ('number_of_purchases_with_specific_department', 'Number of Classrooms with Specific Department'), ('number_of_purchases_with_specific_category', 'Number of Classrooms with Specific Category')], max_length=255),
        ),
    ]
