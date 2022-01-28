from abc import ABC
from datetime import timedelta
from typing import Optional

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from rollcall.models import Rollout
from rollcall.rollout_utils import RolloutUtils
from rollcall.tests import utils


class RolloutUtilsTest(TestCase, ABC):
    def setUp(self) -> None:
        self.user = utils.create_user()
        self.now = timezone.now().replace(hour=15, minute=0, second=0)

    def _create_rollout(self, offset: Optional[timedelta] = None, user: Optional[User] = None) -> Rollout:
        if offset is None:
            offset = timedelta(0)
        if user is None:
            user = self.user
        return Rollout.objects.create(user=user, time=self.now + offset)


class DayRolloutsTest(RolloutUtilsTest):
    def test_today_rollouts_should_not_contain_rollouts_of_other_days(self):
        self._create_rollout(offset=-timedelta(days=1))
        self._create_rollout()
        today_rollouts = RolloutUtils.get_rollouts_of_day(self.now)
        self.assertEqual(len(today_rollouts), 1)

    def test_today_rollouts_of_user_should_not_contain_rollouts_of_other_users(self):
        user2 = utils.create_user(username='user2')
        self._create_rollout()
        self._create_rollout(user=user2)
        today_rollouts = RolloutUtils.get_rollouts_of_day(self.now, self.user)
        self.assertEqual(len(today_rollouts), 1)

    def test_today_rollouts_should_return_all_rollouts_of_today(self):
        for i in range(3):
            self._create_rollout(offset=timedelta(minutes=i))
        today_rollouts = RolloutUtils.get_rollouts_of_day(self.now, self.user)
        self.assertEqual(len(today_rollouts), 3)


class UserCheckinStatusTest(RolloutUtilsTest):
    def _test_user_has_correct_checkin_status(self, rollouts_count: int, should_be_checked_in: bool):
        for _ in range(rollouts_count):
            self._create_rollout()
        is_checked_in = RolloutUtils.is_checked_in(self.user)
        self.assertEqual(is_checked_in, should_be_checked_in)

    def test_user_without_rollout_should_be_reported_checked_out(self):
        self._test_user_has_correct_checkin_status(rollouts_count=0, should_be_checked_in=False)

    def test_user_with_1_rollout_should_be_reported_checked_in(self):
        self._test_user_has_correct_checkin_status(rollouts_count=1, should_be_checked_in=True)

    def test_user_with_2_rollout_should_be_reported_checked_out(self):
        self._test_user_has_correct_checkin_status(rollouts_count=2, should_be_checked_in=False)

    def test_user_with_3_rollout_should_be_reported_checked_in(self):
        self._test_user_has_correct_checkin_status(rollouts_count=3, should_be_checked_in=True)

    def test_user_with_4_rollout_should_be_reported_checked_out(self):
        self._test_user_has_correct_checkin_status(rollouts_count=4, should_be_checked_in=False)

    def test_user_with_5_rollout_should_be_reported_checked_in(self):
        self._test_user_has_correct_checkin_status(rollouts_count=5, should_be_checked_in=True)

    def test_user_with_6_rollout_should_be_reported_checked_out(self):
        self._test_user_has_correct_checkin_status(rollouts_count=6, should_be_checked_in=False)
