from django.test import TestCase, Client
from posts.models import Post
from django.contrib.auth import get_user_model
User = get_user_model()


class PostsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test_user@test.ru', password='testpass1')
        #создаем тестовый пост, который потом будет использоваться для тестов
        self.post = Post.objects.create(text='The test post', author=self.user)

#После регистрации пользователя создается его персональная страница (profile)
    def test_profile(self):
        # формируем GET-запрос к странице профиля тестового пользователя
        response = self.client.get('/test_user/')
        self.assertEqual(response.status_code, 200)

#Авторизованный пользователь может опубликовать пост (new)
    def test_logged_in(self):
        new_post_text = 'The new test post'
        self.client.login(username='test_user', password='testpass1')
        # отправляем запрос на создание нового тестового поста
        response_new_post_page = self.client.post('/new/', {'text': new_post_text})
        self.assertEqual(response_new_post_page.status_code, 302)
        # проверяем - появился ли текст нового поста на странице
        response_main_page = self.client.get('/')
        self.assertContains(response_main_page, text=new_post_text)

#Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
    def est_not_logged_in(self):
        self.client.logout()
        response = self.client.get('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/')

# После публикации поста новая запись появляется на главной странице сайта (index),
# на персональной странице пользователя (profile), и на отдельной странице поста (post)
    def test_post(self):
        self.client.login(username='test_user', password='testpass1')
        post_text = 'The new second test post'
        #отправляем запрос на создание еще одного нового поста и проверяем успешно ли
        response_new_post_page = self.client.post(f'/new/', {'text': post_text},)
        self.assertEqual(response_new_post_page.status_code, 302)
        #Берем ID вновь созданного поста
        self.post_id = Post.objects.get(text=post_text).id
        #перебор url для проверки: на главной странице, в профиле и на странице поста
        for url in ('', '/test_user/', f'/test_user/{self.post_id}/'):
            response_post = self.client.get(url)
            self.assertContains(response_post, text=post_text)

    def test_edit_post(self):
        # Авторизованный пользователь может отредактировать свой пост и его содержимое
        # изменится на всех связанных страницах
        self.client.login(username='test_user', password='testpass1')
        # Запрашиваем ID созданного в самом начале тестового поста, который будем редактировать
        self.post_id = Post.objects.get(text='The test post').id
        edited_text = 'The edited test post'
        # отправляем запрос на редактирование тестового поста и потом проверяем его на успешность
        response_edit_post_page = self.client.post(f'/test_user/{self.post_id}/edit/', {'text': edited_text})
        self.assertEqual(response_edit_post_page.status_code, 302)
        #перебор url для проверки: на главной странице, в профиле и на странице поста
        for url in ('', '/test_user/', f'/test_user/{self.post_id}/'):
            response_post = self.client.get(url)
            self.assertContains(response_post, text=edited_text)
