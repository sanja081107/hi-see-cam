from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('validate_order/', validate_order, name='validate_order'),
    path('ordering/', OrderingView.as_view(), name='ordering'),
    path('camera_list/', CameraListView.as_view(), name='camera_list'),
    path('camera_detail/<slug:slug>/', CameraDetailView.as_view(), name='camera_detail'),
    path('not_enough_product/', not_enough_product, name='not_enough_product'),
    path('user_detail/<slug:slug>', user_detail, name='user_detail'),
]

htmx = [
    path('search/', search, name='search'),
    path('checking_form/', checking_form, name='checking_form'),
    path('check_form_username/', check_form_username, name='check_form_username'),
    path('check_form_phone/', check_form_phone, name='check_form_phone'),
    path('check_form_email/', check_form_email, name='check_form_email'),
    path('check_form_address/', check_form_address, name='check_form_address'),
    path('check_form_note/', check_form_note, name='check_form_note'),
]

urlpatterns += htmx
