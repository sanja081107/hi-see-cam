# Generated by Django 4.1.3 on 2023-02-13 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_feedbackphotos_options_remove_feedback_images_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cameras',
            name='sold_count',
            field=models.PositiveIntegerField(default=0, verbose_name='проданное количество'),
        ),
    ]
