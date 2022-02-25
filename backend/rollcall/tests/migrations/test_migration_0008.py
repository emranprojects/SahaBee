from django.conf import settings
from django_test_migrations.contrib.unittest_case import MigratorTestCase


# noinspection PyPep8Naming
class TestDirectMigration(MigratorTestCase):
    migrate_from = ('rollcall', '0007_userdetail_enable_timesheet_auto_send')
    migrate_to = ('rollcall', '0008_userdetail_work_email')

    def prepare(self):
        """Prepare some data before the migration."""
        # Bulk create to bypass user_detail creation signal. Since the signal doesn't use old UserDetail.
        User = self.old_state.apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
        UserDetail = self.old_state.apps.get_model('rollcall', 'UserDetail')
        User.objects.bulk_create([User(username='test', email='test@gmail.com')])
        UserDetail.objects.create(user=User.objects.get(username='test'),
                                  personnel_code="",
                                  manager_name="",
                                  unit="")

    def test_work_email_should_be_same_as_user_email(self):
        UserDetail = self.new_state.apps.get_model('rollcall', 'UserDetail')
        user_detail = UserDetail.objects.get(user__username='test')
        self.assertEqual(user_detail.work_email, 'test@gmail.com')
