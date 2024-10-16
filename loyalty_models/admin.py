from django.contrib import admin
from .models import (
    PointRole, PointRoleGroup, Reward, AdditionalService,
    UserPoint, Tier, UserPointsService
)


class PointRoleInline(admin.TabularInline):
    model = PointRole
    extra = 0  # Removes empty extra forms


class RewardInline(admin.TabularInline):
    model = Tier.reward.through
    extra = 0


@admin.register(PointRole)
class PointRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'point_role_type', 'group', 'priority', 'is_active', 'from_date', 'to_date')
    list_filter = ('point_role_type', 'group', 'is_active')
    search_fields = ('point_role_type', 'group__name')
    autocomplete_fields = ('user', 'group', 'reward', 'user_logs')
    filter_horizontal = ('user', 'reward', 'user_logs')
    actions = ['deactivate_selected', 'activate_selected']

    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_selected.short_description = "Deactivate selected roles"

    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    activate_selected.short_description = "Activate selected roles"


@admin.register(PointRoleGroup)
class PointRoleGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [PointRoleInline]


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value', 'reward_type', 'point', 'discount_limit', 'additional_service')
    list_filter = ('reward_type',)
    search_fields = ('name', 'description')
    autocomplete_fields = ('additional_service',)


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description')
    autocomplete_fields = ('user',)
    filter_horizontal = ('user',)


@admin.register(UserPoint)
class UserPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'point', 'tier')
    list_filter = ('tier',)
    search_fields = ('user__username',)
    autocomplete_fields = ('user', 'tier')


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'min_points')
    search_fields = ('name',)
    inlines = [RewardInline]
    autocomplete_fields = ['reward']
