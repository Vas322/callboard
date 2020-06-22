from django.contrib import admin
from .models import Bb, Rubric


class BbAdmin(admin.ModelAdmin):
    """Класс определяющий отображения атрибутов модели в админке"""
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content', 'price')
    search_fields = ('title', 'content')


class BbInline(admin.StackedInline):
    model = Bb


class RubricAdmin(admin.ModelAdmin):
    inlines = [BbInline]


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric, RubricAdmin)
