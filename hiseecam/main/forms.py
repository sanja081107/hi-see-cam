from django.forms import ModelForm
from django import forms
from .models import *


class OrderProductsForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['products'].empty_label = 'Товары:'

    class Meta:
        model = Order
        fields = ('products',)

        # widgets = {
        #     'products': forms.SelectMultiple(attrs={
        #         'class': 'form-control',
        #     }),
        # }


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            # 'products': forms.Select(attrs={'class': 'form-control', 'multiple': ''}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'количество'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'имя'}),
            'phone': forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'placeholder': 'телефон'}),
            'email': forms.TextInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'почта'}),
            'prise': forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'placeholder': 'цена'}),
        }
