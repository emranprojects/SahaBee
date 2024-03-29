from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token


class Rollout(models.Model):
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)


class UserDetail(models.Model):
    NAME_MAX_LENGTH = 128

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='detail')
    work_email = models.EmailField(unique=False, null=False, blank=True, default='')
    personnel_code = models.CharField(max_length=10)
    manager_name = models.CharField(max_length=NAME_MAX_LENGTH)
    manager_email = models.EmailField(unique=False, null=False, blank=True, default='')
    unit = models.CharField(max_length=32)
    enable_timesheet_auto_send = models.BooleanField(default=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token_and_user_detail(sender, instance=None, created=False, raw=False, **kwargs):
    signal_is_raised_through_loaddata_command = raw
    if created and not signal_is_raised_through_loaddata_command:
        Token.objects.create(user=instance)
        UserDetail.objects.create(user=instance,
                                  personnel_code="",
                                  manager_name="",
                                  unit="")
