from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class CamerasAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'get_html_photo', 'price')
    list_editable = ('description', 'price')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'description', 'photo', 'get_html_photo', 'date_release', 'date_published', 'date_edited', 'price')
    readonly_fields = ('get_html_photo', 'date_published', 'date_edited')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=100>")

    get_html_photo.short_description = 'Миниатюра'

admin.site.register(Cameras, CamerasAdmin)
admin.site.register(Order)

admin.site.site_title = 'Видеонаблюдение'
admin.site.site_header = 'Видеонаблюдение'
admin.site.index_title = 'Administrator'
