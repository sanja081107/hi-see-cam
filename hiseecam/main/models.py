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
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('camera_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'
        ordering = ['-date_published']

