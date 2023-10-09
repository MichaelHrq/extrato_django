from rest_framework import serializers
from .models import User

class AllUserSerializer (serializers.ModelSerializer):
  class Meta: 
    model = User
    fields = ('id','username','email')
