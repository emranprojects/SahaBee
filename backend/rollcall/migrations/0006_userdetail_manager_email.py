# Generated by Django 3.2.3 on 2021-08-21 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rollcall', '0005_alter_rollout_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='manager_email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]
