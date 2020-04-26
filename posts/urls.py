from django.urls import path
from . import views


urlpatterns = [
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('new/', views.new_post, name='new_post'),
    # Профайл пользователя
    path('<username>/', views.profile, name='profile'),
    # Просмотр записи
    path('<username>/<int:post_id>/', views.post_view, name='post'),
    # Редактирование записи
    path('<username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('', views.index, name='index'),
]
