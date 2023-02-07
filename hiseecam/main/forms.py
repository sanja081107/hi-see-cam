from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, ReadOnlyPasswordHashField
from django.forms import ModelForm, Form
from django import forms
from django.urls import reverse_lazy

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
                                              }),
            'note': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Ваши пожелания',
                                           'required': False
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
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    slug = forms.SlugField(label='Ваш ID', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш ID', 'readonly': True}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия (не обязательно)', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    photo = forms.ImageField(label='Фото (не обязательно)', required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'accept': 'image/*'}))
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}))
    mobile = forms.CharField(label='Мобильный телефон', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'id': 'tel', 'maxlength': '18', 'placeholder': 'Телефон'}))
    address = forms.CharField(label='Адрес доставки', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повтор пароля'}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'slug', 'first_name', 'last_name', 'photo', 'email', 'mobile', 'photo', 'address', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    slug = forms.SlugField(label='Ваш ID', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш ID', 'readonly': False}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    photo = forms.ImageField(label='Фото', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'type': 'file', 'accept': 'image/*'}))
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}))
    mobile = forms.CharField(label='Мобильный телефон', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'id': 'tel', 'maxlength': '18', 'placeholder': 'Телефон'}))
    address = forms.CharField(label='Адрес доставки', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес'}))
    password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'slug', 'first_name', 'last_name', 'photo', 'email', 'mobile', 'photo', 'address')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    class Meta:
        model = User


class FeedbackForm(ModelForm):

    class Meta:
        model = Feedback
        fields = ['title', 'comment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Напишите отзыв', 'rows': 4}),
        }
        labels = {
            'title': '',
            'comment': ''
        }


class FeedbackPhotosForm(ModelForm):

    class Meta:
        model = FeedbackPhotos
        fields = ['images']
        widgets = {
            'images': forms.FileInput(attrs={'class': 'form-control', 'multiple': 'multiple'}),
        }
        labels = {
            'images': ''
        }


class FilterCameraForm(Form):
    filter_camera = forms.TypedChoiceField(choices=(('none', 'Не выбрано'), ('price_up', 'По цене (↑)'), ('price_down', 'По цене (↓)'), ('popular', 'Популярность')), empty_value=None)

