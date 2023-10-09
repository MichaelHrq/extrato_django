from django.contrib import admin
from .models import User

class Users(admin.ModelAdmin):
    list_display = ('id','username','email')
    list_display_links = ('id','username')
    search_fields = ('username',)
    list_per_page = 20
admin.site.register(User,Users)
