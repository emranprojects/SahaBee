from datetime import datetime

import openpyxl
import pytz
from django.conf import settings
from django.test import TestCase
from persiantools.jdatetime import JalaliDate

from rollcall.excel_converter import ExcelConverter
from rollcall.models import Rollout
from rollcall.tests import utils


class ExcelConverterTest(TestCase):
    def setUp(self) -> None:
        self.user = utils.create_user()
        self.user.detail.personnel_code = "123"
        self.user.detail.manager_name = "abu test"
        self.user.detail.save()

    def test_rollout_should_be_in_excel(self):
        rollout = Rollout.objects.create(user=self.user)
        time = rollout.time.astimezone(pytz.timezone(settings.TIME_ZONE))
        jdate = JalaliDate(time)
        excel_converter = ExcelConverter(self.user, [rollout], JalaliDate(jdate.year, jdate.month, 1).to_gregorian())
        workbook = openpyxl.load_workbook(excel_converter.get_excel_file())
        sheet = workbook.active
        self.assertEqual(sheet[f'D{4 + jdate.day}'].value, time.strftime('%H:%M'))

    def test_user_details(self):
        jdate = JalaliDate(datetime.now())
        excel_converter = ExcelConverter(self.user, [], JalaliDate(jdate.year, jdate.month, 1).to_gregorian())
        workbook = openpyxl.load_workbook(excel_converter.get_excel_file())
        sheet = workbook.active
        self.assertEqual(sheet['R1'].value, self.user.first_name + ' ' + self.user.last_name)
        self.assertEqual(sheet['R2'].value, self.user.detail.personnel_code)
        self.assertEqual(sheet['R3'].value, self.user.detail.manager_name)