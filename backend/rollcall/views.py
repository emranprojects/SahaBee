import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpResponse
from rest_framework import permissions, authentication, filters
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from rollcall import models
from rollcall.excel_converter import ExcelConverter
from rollcall.models import Rollout
from rollcall.rollout_utils import RolloutUtils
from rollcall.serializers import RolloutSerializer, UserDetailSerializer, UserSerializer, UserPublicSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path="google-user-login", permission_classes=[])
    def google_user_login(self, request, *args, **kwargs):
        google_user_id_token = request.data.get('google_user_id_token')
        try:
            google_user_info = id_token.verify_oauth2_token(google_user_id_token,
                                                            google_requests.Request(),
                                                            settings.GOOGLE_CLIENT_ID)
            if google_user_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer!')
            if not google_user_info['email_verified']:
                raise ValueError('Email not verified!')
            email = google_user_info['email']
            user, newly_created = User.objects.get_or_create(email=email, defaults={
                'first_name': google_user_info.get('given_name'),
                'last_name': google_user_info.get('family_name'),
                'username': 'google-user-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            })
            token = Token.objects.get(user=user)
            return Response({'username': user.username,
                             'token': token.key})
        except ValueError as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path="register", permission_classes=[])
    def register(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(methods=['GET', 'PUT', 'DELETE'], detail=False, url_path="self")
    def self_user_endpoint(self, request, *args, **kwargs):
        if request.method == "GET":
            return self._get_current_user(request, *args, **kwargs)
        elif request.method == "PUT":
            return self._update_current_user(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self._delete_current_user(request, *args, **kwargs)
        else:
            raise ValueError(f"Unexpected method: {request.method}")

    @action(methods=['GET'], detail=False, url_path="all")
    def all_users_endpoint(self, request, *args, **kwargs):
        all_users = User.objects.prefetch_related('detail').all()
        return Response(UserPublicSerializer(instance=all_users, many=True).data)

    @action(methods=['GET'], detail=False, url_path="checkin-statuses")
    def all_users_checkin_status_endpoint(self, request, *args, **kwargs):
        return Response(RolloutUtils.get_all_users_checkin_statuses())

    @staticmethod
    def _get_current_user(request, *args, **kwargs):
        serializer = UserSerializer(instance=request.user, context={"request": request})
        return Response(serializer.data)

    @staticmethod
    def _update_current_user(request, *args, **kwargs):
        user_data = {key: val for key, val in request.data.items() if key != 'detail'}
        user_detail_data = request.data.get('detail', {})
        user_serializer = UserSerializer(request.user, user_data, partial=True)
        user_detail_serializer = UserDetailSerializer(request.user.detail, user_detail_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_detail_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        user_detail_serializer.save()
        return Response(status=HTTP_200_OK)

    @staticmethod
    def _delete_current_user(request, *args, **kwargs):
        request.user.delete()
        return Response(status=HTTP_200_OK)


class RolloutViewSet(viewsets.ModelViewSet):
    serializer_class = RolloutSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['time']
    ordering = ['-time']

    def get_queryset(self):
        user = self.request.user
        return Rollout.objects.filter(user=user)


class ReportRollouts(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.BasicAuthentication,
                              authentication.SessionAuthentication]

    def get(self, request, username, year, month):
        if request.user.username != username and not request.user.is_superuser:
            return HttpResponse("", status=HTTP_403_FORBIDDEN)
        user = models.User.objects.get(username=username)
        excel_file = ExcelConverter.generate_excel_file(user, year, month)
        response = HttpResponse(File(excel_file),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=timesheet.xlsx'
        return response
