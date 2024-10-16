from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserPoint


def handle_tier_change(user_points):
    rewards = user_points.tier.reward.all()
    for reward in rewards:
        reward.apply_rewards(user_points.user)


@receiver(pre_save, sender=UserPoint)
def check_tier_change(sender, instance, **kwargs):
    if instance.pk:
        # Get the current tier before saving
        try:
            current_instance = UserPoint.objects.get(pk=instance.pk)
            current_tier = current_instance.tier
        except UserPoint.DoesNotExist:
            # If the instance does not exist, it is being created, not updated
            current_tier = None

        # Compare with the new tier to be saved
        new_tier = instance.tier
        if current_tier != new_tier and new_tier is not None:
            # Tier has changed, call the custom function
            handle_tier_change(instance)
