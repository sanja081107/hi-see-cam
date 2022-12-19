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
