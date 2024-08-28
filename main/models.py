from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    # author = models.CharField(max_length=50, verbose_name='Автор')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Содержимое поста')
    publish_at = models.DateTimeField(default=timezone.now, editable=False)  # editable-не изменяемый
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Изображение')  # указываем имя директории в которой будет храниться изображение, оставляем возможность не обязательного заполнения

    def __str__(self):
        return f'{self.author} - {self.title} - {self.publish_at}'

    def get_absolute_url(self):
        return reverse(viewname='main:post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    """Класс коммент"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'
        ordering = ('created_at',)
