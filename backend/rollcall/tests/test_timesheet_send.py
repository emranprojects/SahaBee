from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone
from persiantools.jdatetime import JalaliDateTime

from rollcall import tasks
from rollcall.models import Rollout
from rollcall.tests import utils


@override_settings(EMAIL_ENABLED=True,
                   TIMESHEETS_RECEIVER_EMAIL='admin.receiver@fake.com')
class TimeSheetPeriodicSendTest(TestCase):
    def setUp(self) -> None:
        self.user = utils.create_user()
        self.user.detail.enable_timesheet_auto_send = True
        self.user.detail.work_email = self.user.email
        self.user.detail.save()
        Rollout.objects.create(user=self.user)
        Rollout.objects.create(user=self.user)
        self._is_today_1st_11th_or_21st_day_of_jalali_month_original = tasks._is_today_1st_11th_or_21st_day_of_jalali_month
        tasks._is_today_1st_11th_or_21st_day_of_jalali_month = lambda: True

    def tearDown(self) -> None:
        tasks._is_today_1st_11th_or_21st_day_of_jalali_month = self._is_today_1st_11th_or_21st_day_of_jalali_month_original

    def test_active_timesheet_send_happy_path(self):
        tasks.send_active_timesheets_if_today_is_appropriate_day_of_month()
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(EMAIL_ENABLED=False)
    def test_active_timesheet_shouldnt_send_when_email_disabled(self):
        tasks.send_active_timesheets_if_today_is_appropriate_day_of_month()
        self.assertEqual(len(mail.outbox), 0)

    def test_active_timesheet_shouldnt_send_when_timesheet_auto_send_disabled(self):
        self.user.detail.enable_timesheet_auto_send = False
        self.user.detail.save()
        tasks.send_active_timesheets_if_today_is_appropriate_day_of_month()
        self.assertEqual(len(mail.outbox), 0)

    def test_email_should_not_send_when_user_has_no_work_email(self):
        self.user.detail.work_email = ''
        self.user.detail.save()
        tasks.send_active_timesheets_if_today_is_appropriate_day_of_month()
        self.assertEqual(len(mail.outbox), 0)


class DetectingAppropriateDaysForSendingTimesheetTest(TestCase):
    APPROPRIATE_DAYS_OF_MONTH_TO_SEND_TIMESHEETS = [1, 11, 21]

    @staticmethod
    def _mock_day_of_month(day_of_month: int):
        return patch.object(timezone, 'now',
                            return_value=JalaliDateTime(year=1400, month=1, day=day_of_month).to_gregorian())

    def test_task_should_detect_appropriate_days_for_sending_timesheet(self):

        for day in range(1, 32):
            with self._mock_day_of_month(day):
                self.assertEqual(tasks._is_today_1st_11th_or_21st_day_of_jalali_month(),
                                 day in self.APPROPRIATE_DAYS_OF_MONTH_TO_SEND_TIMESHEETS)
