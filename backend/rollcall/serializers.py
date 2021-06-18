from django.contrib.auth.hashers import make_password
from drf_recaptcha.fields import ReCaptchaV3Field
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from rollcall.models import Rollout, UserDetail
from django.contrib.auth.models import User


class RolloutSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rollout
        fields = ['id', 'time', 'user']
        extra_kwargs = {'user': {'required': False}}

    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        return super().create(validated_data)


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['personnel_code', 'manager_name', 'unit', 'user']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})
    email = serializers.EmailField()
    recaptcha = ReCaptchaV3Field(action="register")

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'recaptcha']

    def validate(self, attrs):
        attrs.pop('recaptcha')
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
