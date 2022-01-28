from django.core import mail
from django.test import TestCase, override_settings

from rollcall import tasks
from rollcall.models import Rollout
from rollcall.tests import utils


@override_settings(EMAIL_ENABLED=True,
                   TIMESHEETS_RECEIVER_EMAIL='admin.receiver@fake.com')
class TimeSheetPeriodicSendTest(TestCase):
    def setUp(self) -> None:
        self.user = utils.create_user()
        self.user.detail.enable_timesheet_auto_send = True
        self.user.detail.save()
        Rollout.objects.create(user=self.user)
        Rollout.objects.create(user=self.user)

    def test_active_timesheet_send_happy_path(self):
        tasks.send_active_timesheets()
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(EMAIL_ENABLED=False)
    def test_active_timesheet_shouldnt_send_when_email_disabled(self):
        tasks.send_active_timesheets()
        self.assertEqual(len(mail.outbox), 0)

    def test_active_timesheet_shouldnt_send_when_timesheet_auto_send_disabled(self):
        self.user.detail.enable_timesheet_auto_send = False
        self.user.detail.save()
        tasks.send_active_timesheets()
        self.assertEqual(len(mail.outbox), 0)

    def test_email_is_sent_from_users_address(self):
        tasks.send_active_timesheets()
        self.assertEqual(mail.outbox[0].from_email, self.user.email)

    def test_email_should_not_send_when_user_has_no_email(self):
        self.user.email = ''
        self.user.save()
        tasks.send_active_timesheets()
        self.assertEqual(len(mail.outbox), 0)
