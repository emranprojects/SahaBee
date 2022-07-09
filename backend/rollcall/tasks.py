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
def send_active_timesheets_if_today_is_appropriate_day_of_month():
    if not _is_today_1st_11th_or_21st_day_of_jalali_month():
        logging.info("Sending active timesheets ignored, since today is not an appropriate date.")
        return
    if not settings.EMAIL_ENABLED:
        logging.info("Sending active timesheets ignored, since email is not enabled.")
        return
    least_active_dt = timezone.now() - timedelta(
        seconds=settings.MAX_SECONDS_FROM_LAST_ROLLCALL_TO_CONSIDER_TIMESHEET_AS_ACTIVE)
    user_ids_with_active_timesheet = Rollout.objects \
        .filter(time__gte=least_active_dt) \
        .values_list('user_id', flat=True) \
        .distinct()
    users = User.objects.filter(pk__in=user_ids_with_active_timesheet) \
        .filter(detail__enable_timesheet_auto_send=True)
    logging.info(f"Going to send timesheets of {len(users)} users...")
    for user in users:
        logging.debug(f"Going to send the timesheet of user: {user.username}")
        _send_user_timesheet(user)


def _is_today_1st_11th_or_21st_day_of_jalali_month() -> bool:
    current_day = JalaliDateTime(timezone.now()).day
    return current_day in [1, 11, 21]


def _send_user_timesheet(user):
    j_now = JalaliDateTime.now()
    if not user.detail.work_email:
        logging.info(f"User ({user.username}) work email not found. Emailing the corresponding timesheet ignored.")
        return
    receiver_email = user.detail.work_email

    if j_now.day == 1:
        # The timesheet of the previous month should be sent in the first day of each month.
        report_jdatetime = j_now - timedelta(days=1)
    else:
        report_jdatetime = j_now
    timesheet_file = ExcelConverter.generate_excel_file(user, report_jdatetime.year, report_jdatetime.month).getvalue()
    body_text = f'''Hello, Here is the timesheet of you at SahaBee. As soon as possible, forward this email to the Edari
    This email is sent automatically by SahaBee, since the user was actively rollcalling at SahaBee during the last few days.

User Information:
First name: {user.first_name}
Last name: {user.last_name}
Personnel code: {user.detail.personnel_code}
Username (at SahaBee): {user.username}

Sincerely,
SahaBee

-----------------------
Let the good times roll!
https://sahabee.ir
'''
    message = EmailMessage('SahaBee User Timesheet',
                           body_text,
                           from_email='sahabee@mymail.sahab.ir',
                           to=receiver_email,
                           attachments=[(f'timesheet-{user.detail.personnel_code}.xlsx',
                                         timesheet_file,
                                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')])
    message.send()
    logging.info(f"Successfully emailed timesheet of '{user.username}' to '{settings.TIMESHEETS_RECEIVER_EMAIL}'.")
