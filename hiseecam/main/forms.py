from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
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
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    slug = forms.SlugField(label='Ваш ID', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш ID', 'readonly': True}))
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    email = forms.CharField(label='Почта', required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}))
    mobile = forms.CharField(label='Мобильный телефон', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'id': 'tel', 'maxlength': '18', 'placeholder': 'Телефон'}))
    photo = forms.ImageField(label='Фото', required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'accept': 'image/*'}))
    address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повтор пароля'}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'slug', 'first_name', 'last_name', 'email', 'mobile', 'photo', 'address', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    class Meta:
        model = User
