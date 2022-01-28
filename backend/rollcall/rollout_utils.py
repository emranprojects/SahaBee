from datetime import datetime, timedelta
from typing import Dict, Optional

from django.contrib.auth.models import User
from django.db.models import Count, QuerySet
from django.utils import timezone

from rollcall.models import Rollout


class RolloutUtils:
    @staticmethod
    def get_rollouts_of_day(d: datetime, user: Optional[User] = None) -> QuerySet:
        """
        :param d: The day to search rollouts for. Although, the date is needed for this method,
        but the given argument should be of type datetime (not date) to avoid timezone day difference.
        :param user:
        :return:
        """
        current_day_first_time = d.replace(hour=0, minute=0, second=0, microsecond=0)
        next_day_last_time = current_day_first_time + timedelta(days=1)
        current_day_rollouts = Rollout.objects \
            .filter(time__gte=current_day_first_time) \
            .filter(time__lt=next_day_last_time)
        if user is not None:
            current_day_rollouts = current_day_rollouts.filter(user=user)
        return current_day_rollouts

    @staticmethod
    def is_checked_in(user: User) -> bool:
        today_rollouts = RolloutUtils.get_rollouts_of_day(timezone.now(), user)
        return today_rollouts.count() % 2 == 1

    @staticmethod
    def get_all_users_checkin_statuses() -> Dict[int, bool]:
        """
        :return: {user_id: is_checked_in} dictionary
        """
        today_rollouts = RolloutUtils.get_rollouts_of_day(timezone.now())
        user_rollout_counts_query = today_rollouts.values('user_id').annotate(rollouts_count=Count('user_id')).order_by()
        user_rollout_counts = {item['user_id']: item['rollouts_count'] for item in user_rollout_counts_query}
        user_ids = User.objects.values_list('id', flat=True)
        for user_id in user_ids:
            if user_id not in user_rollout_counts.keys():
                user_rollout_counts[user_id] = 0
        is_checked_ins = {}
        for user_id, rollouts_count in user_rollout_counts.items():
            is_checked_ins[user_id] = rollouts_count % 2 == 1
        return is_checked_ins
