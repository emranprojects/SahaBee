from django.shortcuts import render
from django.contrib.auth.models import User
from rollcall.models import Rollout
from rest_framework import viewsets
from rest_framework import permissions, status
from rollcall.serializers import UserSerializer, RolloutSerializer
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RolloutViewSet(viewsets.ModelViewSet):
    serializer_class = RolloutSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Rollout.objects.filter(user=user)
    