# Generated by Django 3.0.2 on 2020-06-03 19:55

import apps.bboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0007_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='img',
            field=models.ImageField(height_field=100, upload_to=apps.bboard.models.get_timestamp_path, verbose_name='Изображение', width_field=100),
        ),
    ]