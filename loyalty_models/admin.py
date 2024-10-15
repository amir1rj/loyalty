from django.contrib import admin

# Register your models here.
from .models import AdditionalService, PointRole, PointRoleGroup, UserPoints, Rewards, Tiers

admin.site.register(Rewards)
admin.site.register(AdditionalService)
# admin.site.register(PointRole)
admin.site.register(PointRoleGroup)
admin.site.register(Tiers)
admin.site.register(UserPoints)


@admin.register(PointRole)
class PointRoleAdmin(admin.ModelAdmin):
    list_display = ["__str__", "priority", 'is_active']
