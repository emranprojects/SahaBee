from datetime import datetime, date, timedelta

from django.contrib.auth.models import User
from django.db.models import QuerySet

from rollcall.models import Rollout


def get_rollouts_of_day(d: date, user: User) -> QuerySet:
    current_day_first_time = datetime(year=d.year, month=d.month, day=d.day,
                                      hour=0, minute=0, second=0, microsecond=0)
    next_day_last_time = current_day_first_time + timedelta(days=1)
    current_day_rollouts = Rollout.objects \
        .filter(user=user) \
        .filter(time__gte=current_day_first_time) \
        .filter(time__lt=next_day_last_time)
    return current_day_rollouts
