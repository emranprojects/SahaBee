from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase

from rollcall.models import UserDetail, Rollout
from rollcall.tests import utils

SELF_USER_API_URL = '/users/self/'
ALL_USERS_API_URL = '/users/all/'


class UserDetailTest(TestCase):
    def test_user_detail_should_be_created_on_creating_user(self):
        user = User.objects.create(username='username',
                                   first_name=f'firstname',
                                   last_name=f'lastname')
        self.assertTrue(UserDetail.objects.filter(user=user).exists())


class UserUpdateAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = utils.create_user()
        self.client.force_login(self.user)

    def test_id_shouldnt_update(self):
        user_id = self.user.id
        detail_id = self.user.detail.id
        self.client.put(SELF_USER_API_URL, data={
            'id': user_id + 1,
            'detail': {
                'id': detail_id + 1,
            }
        }, format='json')
        self.user.refresh_from_db()
        self.assertEqual(self.user.id, user_id)
        self.assertEqual(self.user.detail.id, detail_id)

    def test_user_can_be_updated(self):
        resp = self.client.put(SELF_USER_API_URL, data={
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
        resp = self.client.put(SELF_USER_API_URL, data={
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


class UserGetAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = utils.create_user()
        self.client.force_login(self.user)

    def test_user_can_be_retrieved(self):
        resp = self.client.get(SELF_USER_API_URL)
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertEqual(resp.data['id'], self.user.id)


class AllUsersGetAPITest(APITestCase):
    def setUp(self) -> None:
        self.authenticated_user = utils.create_user()
        self.client.force_login(self.authenticated_user)

    def test_can_get_all_users(self):
        utils.create_user(username='user1')
        resp = self.client.get(ALL_USERS_API_URL)
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_should_not_return_detail_field_of_others(self):
        utils.create_user(username='user1')
        resp = self.client.get(ALL_USERS_API_URL)
        user1 = next(user for user in resp.data if user['username'] == 'user1')
        self.assertIsNone(user1.get('detail'))


class UserDeleteAPITest(APITestCase):
    def setUp(self) -> None:
        self.user = utils.create_user()
        self.client.force_login(self.user)

    def test_delete_returns_401_when_not_logged_in(self):
        self.client.logout()
        resp = self.client.delete(SELF_USER_API_URL)
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)

    def test_can_delete_self(self):
        self.assertTrue(User.objects.filter(id=self.user.pk).exists())
        resp = self.client.delete(SELF_USER_API_URL)
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertFalse(User.objects.filter(id=self.user.pk).exists())

    def test_user_is_not_authenticated_anymore_after_getting_deleted(self):
        resp = self.client.delete(SELF_USER_API_URL)
        self.assertEqual(resp.status_code, HTTP_200_OK)
        resp = self.client.get(SELF_USER_API_URL)
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)

    def test_can_delete_self_when_having_rollouts(self):
        rollout = Rollout.objects.create(user=self.user)
        self.test_can_delete_self()
