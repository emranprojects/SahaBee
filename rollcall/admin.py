from django.contrib import admin
from rollcall.models import Rollout

@admin.register(Rollout)
class RolloutAdmin(admin.ModelAdmin):
    fields = ('user', 'time')
    list_display = ('time', 'user')