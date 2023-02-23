from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('cart_add_one_camera_detail/<int:product_id>/', views.cart_add_one_camera_detail, name='cart_add_one_camera_detail'),
    path('cart_add_one_camera_list/<int:product_id>/', views.cart_add_one_camera_list, name='cart_add_one_camera_list'),
    path('check_add_in_basket/<int:product_id>/', views.check_add_in_basket, name='check_add_in_basket'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.clear, name='clear'),
    # path('print_cart/', views.print_cart, name='print_cart'),
]
