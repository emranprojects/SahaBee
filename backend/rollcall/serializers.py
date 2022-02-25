from datetime import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from drf_recaptcha.fields import ReCaptchaV3Field
from persiantools.jdatetime import JalaliDateTime
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rollcall.models import Rollout, UserDetail
from django.contrib.auth.models import User

from rollcall.rollout_utils import RolloutUtils


class RolloutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rollout
        fields = ['id', 'time', 'user']
        extra_kwargs = {'user': {'required': False}}

    def validate(self, attrs):
        super().validate(attrs)
        time = attrs.get('time', timezone.now())
        self._validate_time(time)
        return attrs

    @property
    def _user(self):
        return self.context["request"].user

    def _validate_time(self, time: datetime):
        current_rollouts_count = RolloutUtils.get_rollouts_of_day(time, self._user).count()
        if current_rollouts_count >= settings.MAX_ROLLOUTS_PER_DAY:
            raise serializers.ValidationError(
                f"Too many rollouts for this single day! (max rollouts per day: {settings.MAX_ROLLOUTS_PER_DAY})")

    def create(self, validated_data):
        validated_data['user'] = self._user
        return super().create(validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['id', 'work_email', 'personnel_code', 'manager_name', 'manager_email', 'unit',
                  'enable_timesheet_auto_send']


class UserPublicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class UserSerializer(UserPublicSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})
    recaptcha = ReCaptchaV3Field(action="register")
    detail = UserDetailSerializer(read_only=True)

    class Meta(UserPublicSerializer.Meta):
        fields = UserPublicSerializer.Meta.fields + ['password', 'email', 'recaptcha', 'detail']

    def validate(self, attrs):
        attrs.pop('recaptcha', None)
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
