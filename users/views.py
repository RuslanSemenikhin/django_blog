from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from blog.settings import LOGIN_REDIRECT_URL
from django.urls import reverse
# Create your views here.


def register(request):
    # если нажали кнопку "Регистрация" (метод Post)
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():  # проверка валидности формы (создание словаря с данными формы cleaned data)
            new_user = user_form.save(commit=False)  # если True, то сразу сохранит в БД
            new_user.set_password(user_form.cleaned_data['password'])  # устанавливаем пароль для
            new_user.save()  # сохраняем в БД, по умолчанию commit=True

            context = {'title': 'Успешная регистрация', 'new_user': new_user}
            return render(request, template_name='users/register_done.html', context=context)
    # если просто прогружаем страницу регистрации (GET)
    user_form = UserRegistrationForm()
    context = {'title': 'Регистрация пользователя', 'register_form': user_form}
    return render(request, template_name='users/register.html', context=context)


def log_in(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)  # аутентификация (проверка наличия пользователя и соответствия пароля)
        if user is not None:
            login(request, user)  # авторизация (вход и получение прав доступа, подгрузка параметров пользователя)
            url = request.GET.get('next', LOGIN_REDIRECT_URL)  # для возможности перекидывать откуда пришел
            return redirect(url)
    return render(request, 'users/login.html', {'form': form})


def log_out(request):
    """Функция выхода из аккаунта (сессии)"""
    logout(request)
    url = reverse('main:posts')  # передаем приложение и наименовани url адреса
    return redirect(url)  # переходим на главную страницу после выхода (полученный url ранее)


def get_user_info(request, pk):
    user = User.objects.get(pk=pk)
    context = {'user': user}
    return render(request, 'users/user.html', context=context)

