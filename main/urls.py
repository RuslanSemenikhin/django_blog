from django.urls import path
from .views import (posts,
                    post_add,
                    post_detail,
                    post_update,
                    post_delete_confirm,
                    comment_edit)

app_name = 'main'  # создаем для того, чтоб была некая ссылка на приложение использующее фору, view
urlpatterns = [
    path('', posts, name='posts'),
    path('posts/', post_add, name='create post'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('posts/<int:pk>/update/', post_update, name='post_update'),
    path('posts/<int:pk>/delete/confirm/', post_delete_confirm, name='post_delete_confirm'),

    path('posts/<int:post_id>/comments/<int:comment_id>/edit/', comment_edit, name='comment_edit'),
    # path('posts/<int:post_id>/comments/<int:comment_id>/delete/', ,name='comment_delete'),
]

