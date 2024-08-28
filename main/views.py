from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def posts(request):
    # print(request, '<----')
    title = 'Посты'
    posts = Post.objects.all()
    context = {'title': title, 'posts': posts}
    return render(request, template_name='main/posts.html', context=context)

# @login_required
# def post_add(request):
#     """
#     GET - methods
#     1. создать пустую форму для заполнения form = PostForm()
#     2. передать пустую форму в контексте в шаблон post_add.html
#     POST - methods
#     3. валидация данных формы (проверка данных(длина...)) и внесение изменения при необходимости
#     4. сохранение данных формы в БД
#     5. return post_list
#     """
#     title = 'Добавить пост'
#     if request.method == 'GET':  # request.method - позволяет определить тип запроса get, post
#         form = PostForm(initial={'author': request.user.username})
#         context = {'title': title, 'form': form}
#         return render(request, 'main/new_post.html', context=context)
#     if request.method == 'POST':
#         post_form = PostForm(request.POST, request.FILES)  # request.FILES - если нужно еще подгрузить изображение/файл
#         # далее процедура валидация, проверка полей на качество заполнения
#         # на этом этапе можем дозаполнить данными форму (пример: возраст)
#         if post_form.is_valid():
#             # если валидация прошла, то заполняется словарь cleaned_data
#             post = Post()
#             post.author = request.user
#             post.title = post_form.cleaned_data['title']
#             post.text = post_form.cleaned_data['text']
#             post.image = post_form.cleaned_data['image']
#             post.save()
#             return posts(request)
#             # return render(request, 'main/posts.html')


@login_required
def post_add(request):
    title = 'Добавить пост'
    if request.method == 'GET':
        form = PostForm(author=request.user)
        context = {"title": title, "form": form}
        return render(request, template_name="main/new_post.html", context=context)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, author=request.user)
        if post_form.is_valid():
            # post = Post()
            # post.author = request.user
            # post.title = post_form.cleaned_data['title']
            # post.text = post_form.cleaned_data['text']
            # post.image = post_form.cleaned_data['image']
            # post.save()
            post_form.save()
            # instance = post_form.save(commit=False)
            # #instance.author = request.user  # Сохраняем пользователя вместе с формой
            # instance.save()
            return posts(request)


def post_detail(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    title = "Информация о посте"
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(to='main:post_detail', pk=pk)
    else:
        form = CommentForm()
    context = {
        'post': post,
        'title': title,
        'comments': comments,
        'form': form
    }
    return render(request, template_name='main/post_detail.html', context=context)


def post_update(request, pk: int):
    """Функция обновления поста"""
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied
    title = 'Редактирование поста'
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        # form = PostForm(request.POST, request.FILES, initial=post)  # было
        if form.is_valid():
            form.save()
            return redirect(to="main:post_detail", pk=pk)
    form = PostForm(instance=post)
    # form = PostForm(initial=post)  # было
    context = {
        'form': form
               }
    return render(request, template_name='main/post_update.html', context=context)


def post_delete_confirm(request, pk: int):
    """Ф-ция доп вопроса при удалении"""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        context = {
            'post': post
        }
        return render(request, template_name='main/post_delete_confirm.html', context=context)
    if post.author == request.user:
        post.delete()
        return redirect(to='main:posts')
    raise PermissionDenied


def comment_add(request):
    """Ф-ция добавления коммента"""

    pass


def comment_edit(request, post_id: int, comment_id: int):
    """"""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(to='main:post_detail', pk=post_id)
    else:
        form = CommentForm(instance=comment)
        return render(request, template_name='main/edit_comment.html', context={'form': form})


def comment_delete(request, post_id: int, comment_id: int):
    """Для дз"""
    pass

def handler404(request, exception):
    context = {
        'title': 'Страница не найдена',
        'text': 'Страница не найдена',
    }
    return render(request, template_name='main/page_404.html', context=context)


def handler403(request, exception):
    context = {
        'title': 'В доступе отказано',
        'text': 'В доступе отказано',
    }
    return render(request, template_name='main/page_403.html', context=context)