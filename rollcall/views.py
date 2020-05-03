from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpResponse
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView

from rollcall import models
from rollcall.excel_converter import ExcelConverter
from rollcall.models import Rollout, UserDetail
from rollcall.serializers import RolloutSerializer, UserDetailSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class RolloutViewSet(viewsets.ModelViewSet):
    serializer_class = RolloutSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Rollout.objects.filter(user=user)


class ReportRollouts(APIView):
    def get(self, request, username, year, month, format=None):
        user = models.User.objects.get(username=username)
        total_days = JalaliDate.days_in_month(month=month, year=year)
        date_from = JalaliDateTime(year=year, month=month, day=1).to_gregorian()
        date_to = JalaliDateTime(year=year, month=month, day=total_days, hour=23,minute=59,second=59,microsecond=999999).to_gregorian()
        rollouts = Rollout.objects\
                    .filter(user=user)\
                    .filter(time__gte=date_from,
                            time__lte=date_to)\
                    .order_by('time')
                    
        excel_file = ExcelConverter(user, rollouts, starting_date=date_from).get_excel_file()
        response = HttpResponse(File(excel_file), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=timesheet.xlsx'
        return response
    