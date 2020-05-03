from rest_framework import serializers
from rollcall.models import Rollout, UserDetail
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'detail']

class RolloutSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Rollout
        fields = ['id', 'time', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        return super().create(validated_data)
    
class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['personnel_code', 'manager_name', 'unit', 'user']
        