from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from users.views.Users import AllUsers

router = routers.DefaultRouter()
router.register('users', AllUsers)

urlpatterns = [
  path('extrato/admin/', admin.site.urls),
  path('auth/', include('users.urls')),
  re_path('auth/', include('djoser.urls.base')),
  path('extrato/', include(router.urls)),
  path('extrato/', include('extrato.urls'))
]
