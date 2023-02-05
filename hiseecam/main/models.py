from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse


def upload_path_autor(instance, filename):
    return 'photos/feedback/{0}/{1}'.format(instance.post.user.slug, filename)


def upload_camera_photos(instance, filename):
    return 'photos/camera/{0}/{1}'.format(instance.post.slug, filename)


class CustomUser(AbstractUser):
    slug = models.SlugField(verbose_name='Ваш ID', max_length=50, unique=True, db_index=True, null=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', null=True, blank=True)
    mobile = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', null=True, blank=True)

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


class CamerasPhotos(models.Model):
    images = models.ImageField(upload_to=upload_camera_photos, blank=True, verbose_name='фото')
    post = models.ForeignKey(Cameras, related_name='cameras_images', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Все фото'


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True, verbose_name='Пользователь')
    quantity = models.TextField(verbose_name='Количество товара', blank=True)
    username = models.CharField(max_length=50, verbose_name='Ваше имя', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Мобильный телефон', blank=True)
    email = models.EmailField(verbose_name='Почта', blank=True)
    address = models.TextField(verbose_name='Адрес доставки', blank=True, null=True)
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)
    created = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='Цена', blank=True)

    def __str__(self):
        return f'{self.username} - {self.price}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']


class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT, default=None, verbose_name='Пользователь')
    title = models.CharField(max_length=100, verbose_name='Название')
    comment = models.TextField(verbose_name='Ваш отзыв')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f"{self.title} - {self.comment[:15]}..."

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']


class FeedbackPhotos(models.Model):
    images = models.ImageField(upload_to=upload_path_autor, blank=True, verbose_name='Фотографии')
    post = models.ForeignKey(Feedback, related_name='feedback_images', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото отзыва'
        verbose_name_plural = 'Все фото отзыва'
