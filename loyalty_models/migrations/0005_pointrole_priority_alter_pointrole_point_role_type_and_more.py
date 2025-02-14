# Generated by Django 5.1.2 on 2024-10-15 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_models', '0004_pointrole_rewards'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointrole',
            name='priority',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pointrole',
            name='point_role_type',
            field=models.CharField(choices=[('number_of_purchases', 'Number of Classrooms'), ('number_of_purchases_with_specific_classroom', 'Number of Classrooms with Specific Classroom'), ('number_of_purchases_with_specific_department', 'Number of Classrooms with Specific Department'), ('number_of_purchases_with_specific_category', 'Number of Classrooms with Specific Category'), ('number_of_purchases_with_specific_work_group', 'Number of Classrooms with Specific Work Group')], max_length=255),
        ),
        migrations.AlterField(
            model_name='rewards',
            name='reward_type',
            field=models.CharField(choices=[('amount', 'Amount'), ('percentage', 'Percentage'), ('additional_service', 'Additional Service'), ('point', 'Point'), ('amount_on_specific_classroom', 'Amount on Specific Classroom'), ('amount_on_specific_department', 'Amount on Specific Department'), ('amount_on_specific_category', 'Amount on Specific Category'), ('amount_on_specific_work_group', 'Amount on Specific Work Group'), ('percentage_on_specific_classroom', 'Percentage on Specific Classroom'), ('percentage_on_specific_department', 'Percentage on Specific Department'), ('percentage_on_specific_category', 'Percentage on Specific Category'), ('percentage_on_specific_work_group', 'Percentage on Specific Work Group'), ('register_in_specific_classroom', 'Register in Specific Classroom')], max_length=255),
        ),
        migrations.AddConstraint(
            model_name='pointrole',
            constraint=models.UniqueConstraint(fields=('group', 'priority'), name='unique_priority_per_group'),
        ),
    ]
