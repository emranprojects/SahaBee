from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.status import HTTP_201_CREATED


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
