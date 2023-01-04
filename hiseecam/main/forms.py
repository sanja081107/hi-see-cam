from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from .models import *


class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['user'].empty_label = 'Пользователи:'

    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ('created', 'user', 'quantity', 'price')
        widgets = {

            'username': forms.TextInput(attrs={'class': 'form-control f',
                                               'placeholder': 'имя',
                                               'required': True,
                                               'hx-get': "/check_form_username/",
                                               'hx-trigger': "change",
                                               'hx-target': "#check-result"
                                               }),
            'phone': forms.TextInput(attrs={'class': 'form-control f',
                                            'type': 'number',
                                            'placeholder': 'телефон',
                                            'required': True,
                                            'hx-get': "/check_form_phone/",
                                            'hx-trigger': "change",
                                            'hx-target': "#check-result"
                                            }),
            'email': forms.TextInput(attrs={'class': 'form-control f',
                                            'type': 'email',
                                            'placeholder': 'почта',
                                            'required': True,
                                            'hx-get': "/check_form_email/",
                                            'hx-trigger': "change",
                                            'hx-target': "#check-result"
                                            }),
        }

    def clean_username(self):
        title = self.cleaned_data['username']
        if title == '':
            raise ValidationError('Введите имя пользователя')
        return title

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone == '':
            raise ValidationError('Введите номер телефона')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            raise ValidationError('Введите почту')
        return email

