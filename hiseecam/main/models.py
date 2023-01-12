from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    slug = models.SlugField(verbose_name='URL', max_length=50, unique=True, db_index=True, null=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', null=True, blank=True)
    mobile = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    address = models.TextField(verbose_name='Адрес доставки', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.username


class Cameras(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL', null=True)
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото камеры', null=True, blank=True)
    date_published = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    date_edited = models.DateField(auto_now=True, verbose_name='Дата изменения')
    date_release = models.DateField(verbose_name='Дата выпуска')
    quantity = models.IntegerField(verbose_name='Количество', default=0, null=True)
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('camera_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'
        ordering = ['-date_published', 'title']


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True, verbose_name='Пользователь')
    quantity = models.TextField(verbose_name='Количество товара', blank=True)
    username = models.CharField(max_length=50, verbose_name='Ваше имя', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Мобильный телефон', blank=True)
    email = models.EmailField(verbose_name='Почта', blank=True)
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)
    address = models.TextField(verbose_name='Адрес доставки', blank=True, null=True)
    created = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='Цена', blank=True)

    def __str__(self):
        return f'{self.username} - {self.price}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']
