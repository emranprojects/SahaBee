from django.contrib import admin
from rollcall.models import Rollout, UserDetail

@admin.register(Rollout)
class RolloutAdmin(admin.ModelAdmin):
    fields = ('user', 'time')
    list_display = ('time', 'user')
    
@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    fields = ('user', 'name', 'personnel_code', 'unit', 'manager_name')
    list_display = ('user', 'name', 'personnel_code')