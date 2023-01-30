from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import *


class CamerasAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ('title', 'description', 'quantity', 'get_html_photo', 'price')
    list_editable = ('description', 'quantity', 'price')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'description', 'quantity', 'photo', 'get_html_photo', 'date_release', 'date_published', 'date_edited', 'price')
    readonly_fields = ('get_html_photo', 'date_published', 'date_edited')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=100>")
        # else:
        #     return mark_safe("<img src='/static/main/img/no_image.jpg' width=100>")

    get_html_photo.short_description = 'Миниатюра'


class OrderAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ('username', 'quantity', 'phone', 'created', 'price')
    readonly_fields = ('quantity', 'created',)
    list_filter = ('user', 'created')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'get_html_photo', 'email', 'mobile', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    prepopulated_fields = {'slug': ('username',)}
    search_fields = ('email',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'slug', 'first_name', 'last_name', 'email', 'password', 'photo', 'address', 'mobile')}),
        ('Права доступа', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wides',),
            'fields': ('username', 'slug', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{ object.photo.url }' width=50>")
    get_html_photo.short_description = 'Миниатюра'


admin.site.register(Cameras, CamerasAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.site_title = 'Видеонаблюдение'
admin.site.site_header = 'Видеонаблюдение'
admin.site.index_title = 'Administrator'
