from datetime import datetime, timedelta

import openpyxl
import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from persiantools.jdatetime import JalaliDate
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient, APITestCase

from rollcall import tasks
from rollcall.models import Rollout, UserDetail
from rollcall.excel_converter import ExcelConverter


def create_user(username='default.test.user', is_superuser=False):
    user = User.objects.create(username=username,
                               first_name=f'{username} firstname',
                               last_name=f'{username} lastname',
                               is_superuser=is_superuser)
    return user


class UserTest(TestCase):
    def test_user_detail_should_be_created_on_creating_user(self):
        user = User.objects.create(username='username',
                                   first_name=f'firstname',
                                   last_name=f'lastname')
        self.assertTrue(UserDetail.objects.filter(user=user).exists())


class ExcelConverterTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
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


class ReportRolloutsTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user()

    def _download_timesheet(self, username, auth_user=None):
        api_client = APIClient()
        if auth_user is not None:
            api_client.force_authenticate(auth_user)
        resp = api_client.get(f'/{username}/1400/01/timesheet.xlsx')
        return resp

    def test_unauthenticated_user_cant_download_timesheet(self):
        resp = self._download_timesheet('some_user')
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_download_self_timesheet(self):
        resp = self._download_timesheet(self.user.username, self.user)
        self.assertEqual(resp.status_code, HTTP_200_OK)

    def test_authenticated_user_cant_download_others_timesheet(self):
        other_user = create_user('other_user')
        resp = self._download_timesheet(other_user.username, self.user)
        self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    def test_superuser_can_download_others_timesheet(self):
        superuser = create_user('admin.user', is_superuser=True)
        other_user = create_user('other_user')
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


class RolloutsAPITest(APITestCase):
    ROLLOUT_API_URL = '/rollouts/'

    def setUp(self) -> None:
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_rollouts_should_be_sorted_descending(self):
        t = datetime(2000, 1, 1, 20, 0, 0)
        r1 = Rollout.objects.create(user=self.user, time=t - timedelta(days=1))
        r2 = Rollout.objects.create(user=self.user, time=t)
        resp = self.client.get(RolloutsAPITest.ROLLOUT_API_URL)
        self.assertEqual(resp.data[0]['id'], r2.id)
        self.assertEqual(resp.data[1]['id'], r1.id)

    def test_rollcallings_more_than_max_is_denied(self):
        t = datetime(2000, 1, 1, 20, 0, 0)
        max_rollouts = settings.MAX_ROLLOUTS_PER_DAY
        for _ in range(max_rollouts):
            resp = self.client.post(RolloutsAPITest.ROLLOUT_API_URL, {'time': t})
            self.assertEqual(resp.status_code, HTTP_201_CREATED)
        resp = self.client.post(RolloutsAPITest.ROLLOUT_API_URL, {'time': t})
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    def test_rollcallings_more_than_max_is_denied_with_auto_time(self):
        max_rollouts = settings.MAX_ROLLOUTS_PER_DAY
        for _ in range(max_rollouts):
            resp = self.client.post(RolloutsAPITest.ROLLOUT_API_URL)
            self.assertEqual(resp.status_code, HTTP_201_CREATED)
        resp = self.client.post(RolloutsAPITest.ROLLOUT_API_URL)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)


class UserUpdateTest(APITestCase):
    SELF_USER_API_URL = '/users/self/'

    def setUp(self) -> None:
        self.user = create_user()
        self.client.force_login(self.user)

    def test_id_shouldnt_update(self):
        user_id = self.user.id
        detail_id = self.user.detail.id
        self.client.put(UserUpdateTest.SELF_USER_API_URL, data={
            'id': user_id + 1,
            'detail': {
                'id': detail_id + 1,
            }
        }, format='json')
        self.user.refresh_from_db()
        self.assertEqual(self.user.id, user_id)
        self.assertEqual(self.user.detail.id, detail_id)

    def test_user_can_be_updated(self):
        resp = self.client.put(UserUpdateTest.SELF_USER_API_URL, data={
            'username': 'new_test',
            'password': 'new_pass',
            'email': 'new_test@test.com',
        })
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_test')
        self.assertEqual(self.user.password, 'new_pass')
        self.assertEqual(self.user.email, 'new_test@test.com')

    def test_user_detail_can_be_updated(self):
        resp = self.client.put(UserUpdateTest.SELF_USER_API_URL, data={
            'detail': {
                'personnel_code': 'new_code',
                'unit': 'new_unit',
                'manager_name': 'new_manager',
            }
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.detail.personnel_code, 'new_code')
        self.assertEqual(self.user.detail.unit, 'new_unit')
        self.assertEqual(self.user.detail.manager_name, 'new_manager')


class UserGetTest(APITestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client.force_login(self.user)

    def test_user_can_be_retrieved(self):
        resp = self.client.get(UserUpdateTest.SELF_USER_API_URL)
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertEqual(resp.data['id'], self.user.id)


class TimeSheetPeriodicSendTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        Rollout.objects.create(user=self.user)
        Rollout.objects.create(user=self.user)

    def test_active_timesheet_should_send(self):
        send_user_timesheet_called = False
        sent_timesheet_user = None

        def send_user_timesheet_mocked(user, *args, **kwargs):
            nonlocal send_user_timesheet_called
            nonlocal sent_timesheet_user
            send_user_timesheet_called = True
            sent_timesheet_user = user

        tasks._send_user_timesheet = send_user_timesheet_mocked
        with self.settings(EMAIL_ENABLED=True):
            tasks.send_active_timesheets()
        self.assertTrue(send_user_timesheet_called)
        self.assertEqual(self.user, sent_timesheet_user)

    def test_active_timesheet_shouldnt_send_when_email_disabled(self):
        send_user_timesheet_called = False

        def send_user_timesheet_mocked(user, *args, **kwargs):
            nonlocal send_user_timesheet_called
            send_user_timesheet_called = True

        tasks._send_user_timesheet = send_user_timesheet_mocked
        with self.settings(EMAIL_ENABLED=False):
            tasks.send_active_timesheets()
        self.assertFalse(send_user_timesheet_called)
