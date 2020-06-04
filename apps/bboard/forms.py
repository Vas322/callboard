from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django.core import validators

from .models import Bb, Img, Rubric
from django.contrib.auth.models import User


class BbForm(forms.ModelForm):
    """Форма связанная с моделью Bb"""
    title = forms.CharField(label='Название товара')
    content = forms.CharField(label='Описание',
                              widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    empty_label=None,
                                    label='Рубрика', help_text='Не забудьте указать рубрику!',
                                    widget=forms.widgets.Select(attrs={'size': 8}))
    captcha = CaptchaField(label='Введите текст с картинки',
                           error_messages={'invalid': 'Неправильный текст'}, )
    """
    published = forms.DateField(label='Дата публикации',
                                widget=forms.widgets.SelectDateWidget(
                                    empty_label=('Выберите год', 'Выберите месяц', 'Выберите число')))
    """

    def clean(self):
        """Метод поверяет правильность заполненных полей"""
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError(
                'Укажите описание продаваемого товара')
        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError('Цена должна быть более 0!')
        if len(self.cleaned_data['title']) < 5:
            errors['title'] = ValidationError('Название товара не может быть менее 4 символов!')
        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')


class SearchForm(forms.Form):
    """Форма для поиска слова в рубоике"""
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')


class RegisterUserForm(forms.ModelForm):
    """Форма регистрации нового пользователя"""
    password1 = forms.CharField(label='Введите пароль')
    password2 = forms.CharField(label='Введите пароль повторно')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class ImgForm(forms.ModelForm):
    """Форма загрузки изображения"""
    img = forms.ImageField(label='Изображение',
                           validators=[validators.FileExtensionValidator(
                           allowed_extensions=('gif', 'jpg', 'png'))],
                           widget=forms.widgets.ClearableFileInput(attrs={'multiple': True}),
                           error_messages={'invalid_extention': 'Этот формат файлов ' +
                                                                'не поддерживается'})
    desc = forms.CharField(label='Описание',
                           widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'
