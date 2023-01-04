from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('validate_order/', validate_order, name='validate_order'),
    path('ordering/', OrderingView.as_view(), name='ordering'),
    path('camera_list/', CameraListView.as_view(), name='camera_list'),
    path('camera_detail/<slug:slug>/', CameraDetailView.as_view(), name='camera_detail'),
]

htmx = [
    path('search/', search, name='search'),
    path('checking_form/', checking_form, name='checking_form'),
    path('check_form_username/', check_form_username, name='check_form_username'),
    path('check_form_phone/', check_form_phone, name='check_form_phone'),
    path('check_form_email/', check_form_email, name='check_form_email'),
]

urlpatterns += htmx
