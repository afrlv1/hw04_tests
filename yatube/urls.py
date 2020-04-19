from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views

urlpatterns = [
    # раздел администратора
    path("admin/", admin.site.urls, name='admin'),
    # flatpages
    path("about/", include("django.contrib.flatpages.urls")),
    # регистрация и авторизация
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    # импорт из приложения posts
    path("", include("posts.urls")),
]

# добавим новые пути
urlpatterns += [
    path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about'),
    path('about-tech/', views.flatpage, {'url': '/about-tech/'}, name='abouttech'),
]