from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from os.path import splitext
from django.shortcuts import redirect




def get_timestamp_path(instance, filename):
    """функция для хранения файла"""
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])


class Bb(models.Model):
    """Модель, описывающая объявление"""
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание товара')
    price = models.FloatField(default=0, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, related_name='entries',
                               verbose_name='Рубрика')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
            super().delete(*args, **kwargs)



    class Meta:
        """Атрибуты, позволяющие использовать форму множественного/единственного числа 'Объявления' """
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published']


class Rubric(models.Model):
    """Модель, описывающая рубрики объявлений"""
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название рубрики')

    def __str__(self):
        """функция предоставляющая строковое значение модели"""
        return self.name

    class Meta:
        """Атрибуты, позволяющие использовать форму множественного/единственного числа'Рубрики' """
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ['name']  # индекс, по которому будет происходить сортировка


class RevRubric(Rubric):
    """Класс сортировки по названию"""

    class Meta:
        proxy = True
        ordering = ['name']


class AdditionalImage(models.Model):
    """Модель для иллюстраций"""
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Дополнительная иллюстрация'
        verbose_name_plural = 'Дополнительные иллюстрации'


class AdvUser(models.Model):
    """Модель хранящая доп.сведения о зарегистрированном юзере"""
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
