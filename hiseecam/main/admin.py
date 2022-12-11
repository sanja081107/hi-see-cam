from django.contrib import admin
from .models import *


class CamerasAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'photo', 'price')
    list_editable = ('description', 'photo', 'price')

admin.site.register(Cameras, CamerasAdmin)
