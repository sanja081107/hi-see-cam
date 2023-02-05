from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('validate_order/', validate_order, name='validate_order'),
    path('ordering/', OrderingView.as_view(), name='ordering'),
    path('camera_list/', CameraListView.as_view(), name='camera_list'),
    path('camera_detail/<slug:slug>/', CameraDetailView.as_view(), name='camera_detail'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('not_enough_product/', not_enough_product, name='not_enough_product'),

    path('user_detail/<slug:slug>/', UserDetail.as_view(), name='user_detail'),
    path('user_update/<slug:slug>/', UserUpdate.as_view(), name='user_update'),
    path('user_register/', UserRegister.as_view(), name='user_register'),
    path('user_login/', UserLogin.as_view(), name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),

    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('password_change_done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
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
