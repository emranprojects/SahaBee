from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db.models import QuerySet

from rollcall.models import Rollout


def get_rollouts_of_day(d: datetime, user: User) -> QuerySet:
    """
    :param d: The day to search rollouts for. Although, the date is needed for this method,
    but the given argument should be of type datetime (not date) to avoid timezone day difference.
    :param user:
    :return:
    """
    current_day_first_time = d.replace(hour=0, minute=0, second=0, microsecond=0)
    next_day_last_time = current_day_first_time + timedelta(days=1)
    current_day_rollouts = Rollout.objects \
        .filter(user=user) \
        .filter(time__gte=current_day_first_time) \
        .filter(time__lt=next_day_last_time)
    return current_day_rollouts
