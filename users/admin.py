from django.contrib import admin
from .models import Profile

admin.site.register(Profile)

admin.site.site_header = 'Панель управления'
admin.site.site_title = 'Панель управления'