from django.contrib import admin

# Register your models here.
from .models import  AdditionalService, PointRole, PointRoleGroup, UserPoints,Rewards

admin.site.register(Rewards)
admin.site.register(AdditionalService)
admin.site.register(PointRole)
admin.site.register(PointRoleGroup)
admin.site.register(UserPoints)
