from rest_framework import serializers
from rollcall.models import Rollout
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class RolloutSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Rollout
        fields = ['time', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        return super().create(validated_data)
        