import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils import timezone
from persiantools.jdatetime import JalaliDateTime

from rollcall import constants
from rollcall.excel_converter import ExcelConverter
from rollcall.models import Rollout
from sahabee.celery import app


@app.task(name=constants.TASK_SEND_ACTIVE_TIMESHEETS)
def send_active_timesheets():
    if not settings.EMAIL_ENABLED:
        logging.info("Sending active timesheets ignored, since email is not enabled.")
        return
    least_active_dt = timezone.now() - timedelta(
        seconds=settings.MAX_SECONDS_FROM_LAST_ROLLCALL_TO_CONSIDER_TIMESHEET_AS_ACTIVE)
    user_ids_with_active_timesheet = Rollout.objects \
        .filter(time__gte=least_active_dt) \
        .values_list('user_id', flat=True) \
        .distinct()
    users = User.objects.filter(pk__in=user_ids_with_active_timesheet)
    logging.info(f"Going to send timesheets of {len(users)} users...")
    for user in users:
        logging.debug(f"Going to send the timesheet of user: {user.username}")
        _send_user_timesheet(user)


def _send_user_timesheet(user):
    j_now = JalaliDateTime.now()
    EmailMessage('SahaBee User Timesheet',
                 f'''Hello,
Here is the timesheet of a user at SahaBee.
This email is sent automatically, because the user was actively rollcalling at SahaBee during the last few days. 

User info.:
First name: {user.first_name}
Last name: {user.last_name}
Personnel code: {user.detail.personnel_code}
Username (at SahaBee): {user.username}

Sincerely,
SahaBee

-----------------------
Let the good times roll!
https://sahabee.ir
''',
                 to=[settings.TIMESHEETS_RECEIVER_EMAIL],
                 cc=[user.email if user.email else ''],  # TODO: CC managers (Issue #16)
                 attachments=[(f'timesheet-{user.detail.personnel_code}.xlsx',
                               ExcelConverter.generate_excel_file(user, j_now.year, j_now.month).getvalue(),
                               'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')]).send()
    logging.info(f"Successfully emailed timesheet of '{user.username}' to '{settings.TIMESHEETS_RECEIVER_EMAIL}'.")
