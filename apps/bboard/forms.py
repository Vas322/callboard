from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django.core import validators
from django.forms import inlineformset_factory
from .models import Bb, Rubric, AdditionalImage
from django.contrib.auth.models import User


class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'


AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')


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

    class Meta:
        fields = '__all__'
