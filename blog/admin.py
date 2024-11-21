from django.contrib import admin
from . import models

admin.site.register(models.Post)
admin.site.register(models.Type)
admin.site.register(models.Comment)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Banner)