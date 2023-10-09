from users.views.JWT import *
from users.views.Users import *
from django.urls import path

urlpatterns = [
    path("jwt/create/", CustomTokenObtainPairView.as_view()),
    path("jwt/refresh/", CustomTokenRefreshView.as_view()),
    path("jwt/verify/", CustomTokenVerifyView.as_view()),
    path("jwt/delete/", LogoutView.as_view()),
]
