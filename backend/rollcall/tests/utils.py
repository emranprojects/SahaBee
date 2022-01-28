from django.contrib.auth.models import User


def create_user(username='default.test.user', is_superuser=False):
    user = User.objects.create(username=username,
                               email='test@fake.com',
                               first_name=f'{username} firstname',
                               last_name=f'{username} lastname',
                               is_superuser=is_superuser)
    return user
