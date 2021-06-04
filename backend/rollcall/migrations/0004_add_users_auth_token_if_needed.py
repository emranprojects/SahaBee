# Generated by Django 3.2.3 on 2021-05-28 08:40
# Manual Migration
from django.contrib.auth.models import User
from django.db import migrations
from rest_framework.authtoken.models import Token


def create_tokens_if_needed(apps, schema_editor):
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)


def remove_all_tokens(apps, schema_editor):
    Token.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('rollcall', '0003_remove_userdetail_name'),
    ]
    operations = [
        migrations.RunPython(create_tokens_if_needed, remove_all_tokens)
    ]