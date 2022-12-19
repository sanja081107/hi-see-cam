from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('add_one/<int:product_id>/', views.cart_add_one, name='cart_add_one'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.clear, name='clear'),
    path('print_cart/', views.print_cart, name='print_cart'),
]
