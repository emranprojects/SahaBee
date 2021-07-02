"""sahabee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.authtoken import views as rest_framework_views
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rollcall import views
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'userdetails', views.UserDetailViewSet)
router.register(r'rollouts', views.RolloutViewSet, basename='folan')

urlpatterns = [
    path('api-token-auth/', rest_framework_views.obtain_auth_token),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('<username>/<int:year>/<int:month>/timesheet.xlsx', views.ReportRollouts.as_view()),
    path('api-schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
