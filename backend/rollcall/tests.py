from datetime import datetime

import openpyxl
import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from persiantools.jdatetime import JalaliDate
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from rollcall.models import Rollout, UserDetail
from rollcall.excel_converter import ExcelConverter


class ExcelConverterTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test.tst', first_name='test', last_name='unit zade')
        UserDetail.objects.create(user=self.user,
                                  personnel_code='1',
                                  manager_name='test manager',
                                  unit='test department')

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


class ReportRolloutsTest(TestCase):
    def _download_timesheet(self, username, auth_user=None):
        api_client = APIClient()
        if auth_user is not None:
            api_client.force_authenticate(auth_user)
        resp = api_client.get(f'/{username}/1400/01/timesheet.xlsx')
        return resp

    def _create_user(self, username, is_superuser=False):
        user = User.objects.create(username=username,
                                   first_name=f'{username} firstname',
                                   last_name=f'{username} lastname',
                                   is_superuser=is_superuser)
        UserDetail.objects.create(user=user,
                                  personnel_code='1',
                                  manager_name='test manager',
                                  unit='test department')
        return user

    def test_unauthenticated_user_cant_download_timesheet(self):
        resp = self._download_timesheet('some_user')
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_download_self_timesheet(self):
        user = self._create_user('test.tst')
        resp = self._download_timesheet(user.username, user)
        self.assertEqual(resp.status_code, HTTP_200_OK)

    def test_authenticated_user_cant_download_others_timesheet(self):
        user = self._create_user('test.tst')
        other_user = self._create_user('other_user')
        resp = self._download_timesheet(other_user.username, user)
        self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    def test_superuser_can_download_others_timesheet(self):
        superuser = self._create_user('admin.user', is_superuser=True)
        other_user = self._create_user('other_user')
        resp = self._download_timesheet(other_user.username, superuser)
        self.assertEqual(resp.status_code, HTTP_200_OK)


class RegistrationTest(TestCase):
    def test_user_should_be_created_on_registration(self):
        resp = self.client.post('/users/register/',
                                data={
                                    'username': 'test',
                                    'password': 'test',
                                    'email': 'test@test.com',
                                    'recaptcha': 'test'
                                })
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='test').exists())
