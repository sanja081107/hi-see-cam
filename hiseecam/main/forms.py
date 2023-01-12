from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
        exclude = ('created', 'user', 'quantity', 'price', 'note')
        widgets = {

            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'имя',
                                               'required': True,
                                               'hx-get': "/check_form_username/",
                                               'hx-trigger': "keyup change delay:1ms",
                                               'hx-target': "#check-result"
                                               }),
            'phone': forms.TextInput(attrs={'class': 'form-control',
                                            'type': 'tel',
                                            'id': 'tel',
                                            'maxlength': '18',
                                            'placeholder': 'телефон',
                                            'required': True,
                                            'hx-get': "/check_form_phone/",
                                            'hx-trigger': "keyup change delay:1ms",
                                            'hx-target': "#check-result"
                                            }),
            'email': forms.TextInput(attrs={'class': 'form-control',
                                            'type': 'email',
                                            'placeholder': 'почта',
                                            'required': True,
                                            'hx-get': "/check_form_email/",
                                            'hx-trigger': "keyup change delay:1ms",
                                            'hx-target': "#check-result"
                                            }),
            'address': forms.TextInput(attrs={'class': 'form-control',
                                              'type': 'text',
                                              'placeholder': 'адрес доставки',
                                              'required': True,
                                              'hx-get': "/check_form_address/",
                                              'hx-trigger': "keyup change delay:1ms",
                                              'hx-target': "#check-result"
                                              })
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


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'
