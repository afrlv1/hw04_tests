from django.contrib import admin
# Register your models here.
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'group', 'text', 'author', 'pub_date')
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ('text',)
    # добавляем возможность фильтрации по дате и по группе
    list_filter = ('pub_date', 'group',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'title', 'slug', 'description')
    # добавляем интерфейс для поиска по тексту
    list_filter = ('title',)
    empty_value_display = '-пусто-'


# при регистрации модели Post источником конфигурации для неё назначаем класс PostAdmin
admin.site.register(Post, PostAdmin)
# при регистрации модели  Group источником конфигурации для неё назначаем класс GroupAdmin
admin.site.register(Group, GroupAdmin)