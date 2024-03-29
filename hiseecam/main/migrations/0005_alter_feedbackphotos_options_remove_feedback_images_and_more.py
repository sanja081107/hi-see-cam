# Generated by Django 4.1.3 on 2023-02-05 15:05

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_camerasphotos_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedbackphotos',
            options={'verbose_name': 'Фото отзыва', 'verbose_name_plural': 'Все фото отзыва'},
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='images',
        ),
        migrations.AlterField(
            model_name='feedbackphotos',
            name='images',
            field=models.ImageField(blank=True, upload_to=main.models.upload_path_autor, verbose_name='Фотографии'),
        ),
    ]
