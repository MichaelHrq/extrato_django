from users.models import User
from rest_framework import viewsets
from users.serializers import AllUserSerializer
from rest_framework.permissions import IsAdminUser

__all__ = [
    'AllUsers'
]

class AllUsers(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset = User.objects.filter(is_staff=False)
    serializer_class = AllUserSerializer
