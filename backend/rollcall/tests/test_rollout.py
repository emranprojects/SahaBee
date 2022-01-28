from datetime import datetime, timedelta

from django.conf import settings
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase

from rollcall.models import Rollout
from rollcall.tests import utils


class RolloutsAPITest(APITestCase):
    ROLLOUT_API_URL = '/rollouts/'

    def setUp(self) -> None:
        self.user = utils.create_user()
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
