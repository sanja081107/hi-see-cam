# Generated by Django 4.1.3 on 2022-12-18 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cameras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(null=True, unique=True, verbose_name='URL')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото камеры')),
                ('date_published', models.DateField(auto_now_add=True, verbose_name='Дата публикации')),
                ('date_edited', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('date_release', models.DateField(verbose_name='Дата выпуска')),
                ('quantity', models.IntegerField(default=0, null=True, verbose_name='Количество')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Камера',
                'verbose_name_plural': 'Камеры',
                'ordering': ['-date_published', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.TextField(verbose_name='Количество товара')),
                ('username', models.CharField(max_length=50, verbose_name='Имя пользователя')),
                ('phone', models.CharField(max_length=13, verbose_name='Мобильный телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date publication')),
                ('prise', models.PositiveIntegerField(verbose_name='Цена')),
                ('products', models.ManyToManyField(to='main.cameras', verbose_name='Товары')),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-created'],
            },
        ),
    ]
