from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from google.oauth2 import id_token
from requests import Response
from rest_framework.status import HTTP_200_OK


class GoogleUserLoginTest(TestCase):
    def _try_login(self, gmail: str, google_given_name: str, google_family_name: str) -> Response:
        with patch.object(id_token, 'verify_oauth2_token',
                          return_value={
                              'email': gmail,
                              'given_name': google_given_name,
                              'family_name': google_family_name,
                              'iss': 'accounts.google.com',
                              'email_verified': True,
                          }):
            resp = self.client.post('/users/google-user-login/',
                                    data={
                                        'google_user_id_token': 'fake_token'
                                    })
        return resp

    def test_new_user_should_be_created_on_login(self):
        resp = self._try_login(gmail='test@gmail.com', google_given_name='david', google_family_name='testy')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertTrue(User.objects.filter(email='test@gmail.com').exists())

    def test_already_created_user_is_not_modified_on_login(self):
        user = User.objects.create(email='test@gmail.com', first_name='custom', last_name='customized', username='test')
        resp = self._try_login(gmail='test@gmail.com', google_given_name='david', google_family_name='testy')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'custom')
        self.assertEqual(user.last_name, 'customized')
        self.assertEqual(user.username, 'test')
