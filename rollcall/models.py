from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings

class Rollout(models.Model):
    time = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)