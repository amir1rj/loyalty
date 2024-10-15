from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.utils import timezone

from . import constants


class ActivePointRoleManager(models.Manager):
    def get_queryset(self):
        """Override the queryset to return only active point roles."""
        return super().get_queryset().filter(is_active=True)


class PointRole(models.Model):
    min_class_count = models.PositiveIntegerField(null=True, blank=True)
    # classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE,null=True, blank=True)
    # category = models.ForeignKey('Category', on_delete=models.CASCADE,null=True, blank=True)
    # department = models.ForeignKey('Department', on_delete=models.CASCADE,null=True, blank=True)
    # work_group = models.ForeignKey('WorkGroup', on_delete=models.CASCADE,null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    group = models.ForeignKey('PointRoleGroup', on_delete=models.CASCADE, related_name="poit_roles", null=True,
                              blank=True)
    point_role_type = models.CharField(max_length=255, choices=constants.point_role_type)
    reward = models.ManyToManyField('Rewards', blank=True, related_name='point_roles')
    priority = models.PositiveIntegerField(null=True, blank=True)
    user = models.ManyToManyField(User, related_name="point_roles", blank=True)
    is_active = models.BooleanField(default=True)
    # Custom managers
    objects = models.Manager()  # Default manager
    active_objects = ActivePointRoleManager()  # Custom manager for active PointRoles
    user_logs = models.ManyToManyField(User, related_name="used_point_roles", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group', 'priority'], name='unique_priority_per_group')
        ]

    # todo: should add validation based on point role types
    def clean(self):
        """Adjust priority if there's a conflict within the same group"""
        if self.group and self.priority:
            # Get all PointRoles in the same group, excluding the current one
            point_roles = PointRole.objects.filter(group=self.group).exclude(pk=self.pk).order_by('priority')
            priorities = [role.priority for role in point_roles]

            # If the priority already exists, shift priorities
            if self.priority in priorities:
                conflicting_role = PointRole.objects.get(group=self.group, priority=self.priority)
                # Adjust the conflicting role's priority to be the next available
                max_priority = max(priorities) if priorities else 0
                conflicting_role.priority = max_priority + 1
                conflicting_role.save()
            # Automatically assign priority if it's not provided
            if self.group and not self.priority:
                # Get the highest priority in the group and assign the next value
                max_priority = \
                    PointRole.objects.filter(group=self.group).aggregate(max_priority=models.Max('priority'))[
                        'max_priority']
                self.priority = (max_priority or 0) + 1
                # Custom validation for min_class_count based on point_role_type
        if self.point_role_type == 'number_of_purchases' and self.min_class_count is None:
            raise ValidationError(
                {'min_class_count': 'This field is required when point_role_type is "number_of_purchases".'})

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method to ensure priorities are handled
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.point_role_type}- {self.group} -{self.pk}"

    def make_role_none_reusable(self, user: User):
        self.user_logs.add(user)
        # add point_roles to all active points for preventing to being used twice
        all_point_role_in_group = self.group.poit_roles.all()

        for role in all_point_role_in_group:
            role.user.add(user)
        return {'success': True, 'message': 'role is active'}

    def is_valid(self, user: User, *args, **kwargs) -> dict:
        """ method to deactivate the role if to_date has passed."""
        if self.to_date and self.to_date < timezone.now().date():
            self.is_active = False  # Automatically set to False if the date has passed
            self.save()
            return {"success": False, "message": "this role has expired"}

            # Check if the user already has this point role
        if self.user.filter(id=user.id).exists():
            return {"success": False, "message": "This user already has this point role."}
        return {"success": True, "message": "role is valid"}

    # add user logs to store point roles that user actually used

    def perform_point_role(self, user: User = None) -> dict:
        if self.point_role_type == "number_of_purchases":
            return self.check_number_of_purchases(user)

    # todo should add course and category and ... for optional parameters for specifying other role
    def check_number_of_purchases(self, user: User) -> dict:
        # todo : should replace with actual number of purchases in specific time period
        number_of_purchases = 5
        is_valid = self.is_valid(user)
        if is_valid.get('success'):
            if number_of_purchases >= self.min_class_count:
                self.make_role_none_reusable(user)
                return {"success": True, "message": "point role performed"}

            return {'success': False, "message": "did not passed the point role"}
        return {"success": False, "message": is_valid.get('message')}


class PointRoleGroup(models.Model):
    name = models.CharField(max_length=255)

    # user = models.ManyToManyField(User, related_name="point_role_groups", blank=True)

    def __str__(self):
        return self.name


class Rewards(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    # classroom = models.ManyToManyField('Classroom', on_delete=models.CASCADE, blank=True)
    # department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    # category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    # work_group = models.ForeignKey('WorkGroup', on_delete=models.CASCADE,null=True, blank=True)
    point = models.IntegerField(null=True, blank=True)
    discount_limit = models.IntegerField(null=True, blank=True)
    additional_service = models.ForeignKey('AdditionalService', on_delete=models.CASCADE, null=True, blank=True)
    reward_type = models.CharField(max_length=255, choices=constants.Reward_type)

    def __str__(self):
        return self.name

    def apply_rewards(self, user: User = None):
        if self.reward_type == "point":
            self.add_point_to_user(user)
        elif self.reward_type == 'additional_service':
            self.add_additional_service(user)

    def add_point_to_user(self, user: User) -> dict:
        user.points.add_point(self.point)
        return {"success": True, "message": "points_added"}

    def add_additional_service(self, user: User) -> dict:
        return self.additional_service.add_user_to_additional_services(user)


class AdditionalService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    user = models.ManyToManyField(User, related_name="AdditionalServices", blank=True)

    def __str__(self):
        return self.name

    def add_user_to_additional_services(self, user):
        """Add a user to the additional service, raise an error if already added."""
        if self.user.filter(id=user.id).exists():
            return {"success": False, "message": f"User {user.username} is already added to {self.name}."}
        self.user.add(user)
        return {'success': True, "message": f"User {user.username} added"}


class UserPoints(models.Model):
    user = models.OneToOneField(User, related_name="points", on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    tier = models.ForeignKey('Tiers', related_name='points', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}-{self.point} points'

    def add_point(self, value: int):
        self.point += value
        # check tier
        self.assign_tier()

    def assign_tier(self):
        # Find the highest tier the user qualifies for based on their points
        qualifying_tiers = Tiers.objects.filter(min_points__lte=self.point).order_by('-min_points')
        if qualifying_tiers.exists():
            # Assign the highest qualifying tier
            new_tier = qualifying_tiers.first()
            if self.tier != new_tier:
                self.tier = new_tier
                self.save()


class Tiers(models.Model):
    name = models.CharField(max_length=255)
    min_points = models.PositiveIntegerField()
    reward = models.ManyToManyField(Rewards, related_name="tiers")

    def __str__(self):
        return self.name


class UserPointsService:
    def __init__(self, user):
        self.user = user
        self.user_points, created = UserPoints.objects.get_or_create(user=user)

    @staticmethod
    def get_all_groups():
        # Fetch all PointRoleGroup instances that have at least one active PointRole
        active_groups_with_roles = PointRoleGroup.objects.prefetch_related(
            Prefetch(
                'poit_roles',
                queryset=PointRole.objects.filter(is_active=True).order_by('priority'),
                to_attr='active_roles'  # Store the prefetched PointRoles in this attribute
            )
        )
        return active_groups_with_roles

    def perform_point_roles(self):
        groups = self.get_all_groups()
        for role_group in groups:
            for role in role_group.active_roles:
                # do action based on type
                is_valid = role.perform_point_role(self.user)
                print(is_valid)
                if is_valid.get('success'):
                    # break if one condition in group succeeded
                    rewards = role.reward.all()
                    for reward in rewards:
                        reward.apply_rewards(self.user)
                    break
