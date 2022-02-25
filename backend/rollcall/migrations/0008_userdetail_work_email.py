from django.db import migrations, models


def move_email_to_work_email(apps, schema_editor):
    # noinspection PyPep8Naming
    UserDetail = apps.get_model('rollcall', 'UserDetail')
    for user_detail in UserDetail.objects.all():
        user_detail.work_email = user_detail.user.email
        user_detail.save()


class Migration(migrations.Migration):
    dependencies = [
        ('rollcall', '0007_userdetail_enable_timesheet_auto_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='work_email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.RunPython(move_email_to_work_email)
    ]
