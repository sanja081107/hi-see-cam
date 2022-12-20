from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('validate_order/', validate_order, name='validate_order'),
    path('ordering/', OrderingView.as_view(), name='ordering'),
    path('camera_list/', CameraListView.as_view(), name='camera_list'),
    path('camera_detail/<slug:slug>/', CameraDetailView.as_view(), name='camera_detail'),
]
