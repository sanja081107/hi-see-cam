from django.db import models

class Cameras(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото камеры', null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Camera'
        verbose_name_plural = 'Cameras'
        ordering = ['title']

