from django.db import models
from django.contrib.auth.models import User

from . import constants


# Create your models here.
class PointRole(models.Model):
    min_class_count = models.PositiveIntegerField(null=True, blank=True)
    # classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE,null=True, blank=True)
    # category = models.ForeignKey('Category', on_delete=models.CASCADE,null=True, blank=True)
    # department = models.ForeignKey('Department', on_delete=models.CASCADE,null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    group = models.ForeignKey('PointRoleGroup', on_delete=models.CASCADE, null=True, blank=True)
    point_role_type = models.CharField(max_length=255, choices=constants.point_role_type)
    rewards = models.ManyToManyField('Rewards',null=True, blank=True)

    def __str__(self):
        return f"{self.point_role_type} -{self.pk}"


class PointRoleGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Rewards(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    # classroom = models.ManyToManyField('Classroom', on_delete=models.CASCADE, null=True, blank=True)
    # department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    # category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    point = models.IntegerField(null=True, blank=True)
    discount_limit = models.IntegerField(null=True, blank=True)
    additional_service = models.ForeignKey('AdditionalService', on_delete=models.CASCADE, null=True, blank=True)
    reward_type = models.CharField(max_length=255, choices=constants.Reward_type)

    def __str__(self):
        return self.name


class AdditionalService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class UserPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
