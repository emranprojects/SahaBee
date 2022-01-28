from django.test import TestCase
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from rollcall.tests import utils


class TimesheetDownloadTest(TestCase):
    def setUp(self) -> None:
        self.user = utils.create_user()

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
        other_user = utils.create_user('other_user')
        resp = self._download_timesheet(other_user.username, self.user)
        self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    def test_superuser_can_download_others_timesheet(self):
        superuser = utils.create_user('admin.user', is_superuser=True)
        other_user = utils.create_user('other_user')
        resp = self._download_timesheet(other_user.username, superuser)
        self.assertEqual(resp.status_code, HTTP_200_OK)
