from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


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
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, blank=True, verbose_name='Пользователь')
    products = models.ManyToManyField(Cameras, verbose_name='Товары')
    quantity = models.TextField(verbose_name='Количество товара')
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=13, verbose_name='Мобильный телефон')
    email = models.EmailField(verbose_name='Почта')
    created = models.DateTimeField(verbose_name='Date publication', auto_now_add=True, blank=True)
    prise = models.PositiveIntegerField(verbose_name='Цена')

    def __str__(self):
        return f'{self.username} - {self.prise}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']
