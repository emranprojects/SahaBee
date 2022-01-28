from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpResponse
from rest_framework import permissions, authentication, filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.views import APIView

from rollcall import models
from rollcall.excel_converter import ExcelConverter
from rollcall.models import Rollout
from rollcall.rollout_utils import RolloutUtils
from rollcall.serializers import RolloutSerializer, UserDetailSerializer, UserSerializer, UserPublicSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path="register", permission_classes=[])
    def register(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(methods=['GET', 'PUT'], detail=False, url_path="self")
    def self_user_endpoint(self, request, *args, **kwargs):
        if request.method == "GET":
            return self._get_current_user(request, *args, **kwargs)
        elif request.method == "PUT":
            return self._update_current_user(request, *args, **kwargs)
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
