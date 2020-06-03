from django.db import models
from django.contrib.auth.models import User


class Bb(models.Model):
    """Модель, описывающая объявление"""
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание товара')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, related_name='entries',
                               verbose_name='Рубрика')

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


class AdvUser(models.Model):
    """Модель хранящая доп.сведения о зарегистрированном юзере"""
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
