from django.forms import ModelForm
from django import forms
from .models import *


class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = 'Пользователи:'

    class Meta:
        model = Order
        fields = '__all__'
        # exclude = ('created', 'user',)
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control f'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control f', 'placeholder': 'количество'}),
            'username': forms.TextInput(attrs={'class': 'form-control f', 'placeholder': 'имя'}),
            'phone': forms.TextInput(attrs={'type': 'number', 'class': 'form-control f', 'placeholder': 'телефон'}),
            'email': forms.TextInput(attrs={'type': 'email', 'class': 'form-control f', 'placeholder': 'почта'}),
            'price': forms.TextInput(attrs={'type': 'number', 'class': 'form-control f', 'placeholder': 'цена'}),
        }


# class OrderProductsForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['products'].empty_label = 'Товары:'
#
#     class Meta:
#         model = Order
#         fields = ('products',)
#         widgets = {
#             'products': forms.SelectMultiple(attrs={
#                 'class': 'form-control',
#             }),
#         }
