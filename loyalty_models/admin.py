from django.contrib import admin

# Register your models here.
from .models import AdditionalService, PointRole, PointRoleGroup, UserPoint, Reward, Tier

admin.site.register(Reward)
admin.site.register(AdditionalService)
# admin.site.register(PointRole)
admin.site.register(PointRoleGroup)
admin.site.register(Tier)
admin.site.register(UserPoint)


@admin.register(PointRole)
class PointRoleAdmin(admin.ModelAdmin):
    list_display = ["__str__", "priority", 'is_active', 'from_date', 'to_date','group']
    list_editable = ['is_active', 'from_date', 'to_date','group','priority']
