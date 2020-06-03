from django.contrib import admin
from .models import Bb, Rubric


class BbAdmin(admin.ModelAdmin):
    """Класс определяющий отображения атрибутов модели в админке"""
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content', 'price')
    search_fields = ('title', 'content')


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
