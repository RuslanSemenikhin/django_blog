from django.contrib.auth.models import User
# импорт встроенной модели пользователя
from django import forms
from datetime import datetime
from blog.settings import DATE_INPUT_FORMATS


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    # test = forms.DateField(label='Тест', widget=forms.DateInput(attrs={'type': 'date'}, format='%d.%m.%Y'), input_formats=['%d.%m.%Y'])  # календарик для выбора даты
# initial=datetime.now().date(),
    def clean_password2(self):
        cd = self.cleaned_data  # словарь с чистыми данными
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        """Делаем переобпределение для русского отображения словари"""
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'email': 'Эл. почта'
        }
        help_texts = {
            'username': 'Только буквы, цифры, @ и _'
        }
        widgets = {
            'username': forms.TextInput,
            'email': forms.EmailInput,
        }

