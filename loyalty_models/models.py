from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.utils import timezone
from simple_history.models import HistoricalRecords

from . import constants


class BaseLoyaltyProgramModel(models.Model):
    # classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE,null=True, blank=True)
    # category = models.ForeignKey('Category', on_delete=models.CASCADE,null=True, blank=True)
    # department = models.ForeignKey('Department', on_delete=models.CASCADE,null=True, blank=True)
    # work_group = models.ForeignKey('WorkGroup', on_delete=models.CASCADE,null=True, blank=True)
    # test_field = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class ActivePointRoleManager(models.Manager):
    def get_queryset(self):
        """Override the queryset to return only active point roles."""
        return super().get_queryset().filter(is_active=True)


class PointRole(BaseLoyaltyProgramModel):
    number = models.PositiveIntegerField(null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    group = models.ForeignKey('PointRoleGroup', on_delete=models.CASCADE, related_name="point_roles", null=True,
                              blank=True)
    point_role_type = models.CharField(max_length=255, choices=constants.point_role_type)
    reward = models.ManyToManyField('Reward', blank=True, related_name='point_roles')
    priority = models.PositiveIntegerField(null=True, blank=True)
    user = models.ManyToManyField(User, related_name="point_roles", blank=True)
    is_active = models.BooleanField(default=True)
    # Custom managers
    objects = models.Manager()  # Default manager
    active_objects = ActivePointRoleManager()  # Custom manager for active PointRoles
    user_logs = models.ManyToManyField(User, related_name="used_point_roles", blank=True)
    history = HistoricalRecords()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group', 'priority'], name='unique_priority_per_group')
        ]
        ordering = ['priority']

    # todo: should add validation based on point role types
    def clean(self):
        """Perform validation for point role type."""
        # Custom validation for min_class_count based on point_role_type
        if self.point_role_type in ['number_of_purchases', 'avg_score'] and self.number is None:
            raise ValidationError({'number': f'This field is required when point_role_type is {self.point_role_type}.'})

    def save(self, *args, **kwargs):
        """Assign priority correctly before saving."""
        if self.group:
            # Get the instance in the group with the same priority
            conflicting_instance = PointRole.objects.filter(
                group=self.group, priority=self.priority
            ).exclude(pk=self.pk).first()

            if conflicting_instance:
                # If there's a conflict, find the next available priority and reassign the conflicting instance
                available_priority = 1
                while PointRole.objects.filter(group=self.group, priority=available_priority).exists():
                    available_priority += 1
                conflicting_instance.priority = available_priority
                conflicting_instance.save()

            # Automatically assign priority if not provided
            if not self.priority:
                # Find the lowest available priority in the group
                taken_priorities = PointRole.objects.filter(group=self.group).values_list('priority', flat=True)
                # Sort and find the first missing priority
                available_priority = 1
                for prio in sorted(taken_priorities):
                    if prio == available_priority:
                        available_priority += 1
                    else:
                        break
                # Assign the lowest available priority
                self.priority = available_priority

        # Now call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.point_role_type}- {self.group} -{self.pk}"

    def make_role_none_reusable(self, user: User):
        # add user logs to store point roles that user actually used
        self.user_logs.add(user)
        # add point_roles to all active points for preventing to being used twice
        all_point_role_in_group = self.group.point_roles.all()
        with transaction.atomic():
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

    def perform_point_role(self, user: User = None) -> dict:
        if self.point_role_type == "number_of_purchases":
            return self.check_number_of_purchases(user)
        if self.point_role_type == "num_of_first_in_class":
            return self.check_number_if_first_in_class(user)
        if self.point_role_type == "avg_score":
            return self.check_avg_score(user)

    # todo should add course and category and ... for optional parameters for specifying other role
    def check_number_of_purchases(self, user: User) -> dict:
        # todo : should replace with actual number of purchases in specific time period
        number_of_purchases = 5
        # Use compare_with_value function for comparison
        return self.compare_with_value(number_of_purchases, 'gte', user)

    # todo should add course and category and ... for optional parameters for specifying other role
    def check_number_if_first_in_class(self, user: User) -> dict:
        # TODO: Replace with actual number of first in class in a specific time period
        number_of_first_in_class = 5

        # Use compare_with_value function for comparison
        return self.compare_with_value(number_of_first_in_class, 'gte', user)

    # todo should add course and category and ... for optional parameters for specifying other role
    def check_avg_score(self, user: User) -> dict:
        # TODO: Replace with actual average score in a specific time period
        avg_score = 78

        # Use compare_with_value function for comparison
        return self.compare_with_value(avg_score, 'gte', user)

    def compare_with_value(self, value, compare_type, user: User) -> dict:
        is_valid = self.is_valid(user)

        if is_valid.get('success'):
            # Handle comparison based on the provided compare_type
            if compare_type == 'gte':  # Greater than or equal to
                if value >= self.number:
                    self.make_role_none_reusable(user)
                    return {"success": True, "message": "point role performed"}
                return {'success': False, "message": "did not pass the point role"}

            elif compare_type == 'lte':  # Less than or equal to
                if value <= self.number:
                    self.make_role_none_reusable(user)
                    return {"success": True, "message": "point role performed"}
                return {'success': False, "message": "did not pass the point role"}

            # Add a fallback for invalid compare_type values
            return {"success": False, "message": "Invalid comparison type"}

        return {"success": False, "message": is_valid.get('message')}

    @property
    def user_point_role_usage_frequency(self):
        return self.user_logs.count()


class PointRoleGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Reward(BaseLoyaltyProgramModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
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


class AdditionalService(BaseLoyaltyProgramModel):
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


class UserPoint(models.Model):
    user = models.OneToOneField(User, related_name="points", on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    tier = models.ForeignKey('Tier', related_name='points', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}-{self.point} points'

    def add_point(self, value: int):
        self.point += value
        self.save()
        # check tier
        self.assign_tier()

    def assign_tier(self):
        # Find the highest tier the user qualifies for based on their points
        qualifying_tiers = Tier.objects.filter(min_points__lte=self.point).order_by('-min_points')
        if qualifying_tiers.exists():
            # Assign the highest qualifying tier
            new_tier = qualifying_tiers.first()
            if self.tier != new_tier:
                self.tier = new_tier
                self.save()


class Tier(models.Model):
    name = models.CharField(max_length=255)
    min_points = models.PositiveIntegerField()
    reward = models.ManyToManyField(Reward, related_name="tiers")

    def __str__(self):
        return self.name


class UserPointsService:
    def __init__(self, user):
        self.user = user
        self.user_points, created = UserPoint.objects.get_or_create(user=user)

    @staticmethod
    def get_all_groups():
        # Fetch all PointRoleGroup instances that have at least one active PointRole
        active_groups_with_roles = PointRoleGroup.objects.prefetch_related(
            Prefetch(
                'point_roles',
                queryset=PointRole.active_objects.prefetch_related('reward').order_by('priority'),
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

                if is_valid.get('success'):
                    # break if one condition in group succeeded
                    for reward in role.reward.all():
                        reward.apply_rewards(self.user)
                    break
