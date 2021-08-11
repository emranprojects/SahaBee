from django.contrib.auth.hashers import make_password
from drf_recaptcha.fields import ReCaptchaV3Field
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rollcall.models import Rollout, UserDetail
from django.contrib.auth.models import User


class RolloutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rollout
        fields = ['id', 'time', 'user']
        extra_kwargs = {'user': {'required': False}}

    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        return super().create(validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['id', 'personnel_code', 'manager_name', 'unit']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})
    email = serializers.EmailField()
    recaptcha = ReCaptchaV3Field(action="register")
    detail = UserDetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'recaptcha', 'detail']

    def validate(self, attrs):
        attrs.pop('recaptcha', None)
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
