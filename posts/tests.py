from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Post
User = get_user_model()


# Зарегистрируем тестового пользователя
class UserTest(TestCase):
    def setUp(self):
        # создание тестового клиента — подходящая задача для функции setUp()
        self.client = Client()
        # создаём пользователя
        self.user = User.objects.create_user(username='test_user_1', email='test_user_1@test.com', password='test12345')
        # Добавляем первую строку
        self.post = Post.objects.create(text='Test string 1', author=self.user)
# Проверяем, что после регистрации пользователя создается его персональная страница (profile)
    def test_profile(self):
        print('testing Profile')
        response = self.client.get('/test_user_1/')
        self.assertEqual(response.status_code, 200)

# Авторизованный пользователь может опубликовать пост (new)
    def test_create_post(self):
        print('testing create post')
        self.client.login(username='test_user_1', password='test12345')
        response = self.client.post('/new/', {'text':'test string 2'})
        self.assertEqual(response.status_code, 302)
        response1 = self.client.get('/')
        self.assertContains(response1, text = 'test string 2')

# Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
    def test_redirect(self):
        print('test redirect')
        response = self.client.get('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/', status_code=302,
                             target_status_code=200, msg_prefix='', fetch_redirect_response=True)

# После публикации поста новая запись появляется на главной странице сайта (index),
# на персональной странице пользователя (profile),
# и на отдельной странице поста (post)
    def test_accept_post(self):
        print('testing accept post')
        self.client.login(username='test_user_1', password='test12345')
        post_text = "test string 3"
        self.post = Post.objects.create(text=post_text, author=self.user)
        post_id = self.post.pk
        response = self.client.get('/') # проверка для главной страницы
        self.assertContains(response, post_text)
        response1 = self.client.get('/test_user_1/') # проверка на профиле
        self.assertContains(response1, post_text)
        response2 = self.client.get(f'/test_user_1/{post_id}/') # проверка для страницы поста
        self.assertContains(response2, post_text)

# Авторизованный пользователь может отредактировать свой пост и его содержимое изменится на всех связанных страницах
    def test_edit_post(self):
        print('testing edit post')
        self.client.login(username='test_user_1', password='12345')
        post_text = "test string 4"
        post_id = self.post.pk
        self.post = Post.objects.create(text=post_text, author=self.user)
        response = self.client.post(f'/test_user_1/{post_id}/edit/', {'text':'test string 4'})
        self.assertEqual(response.status_code, 302)
        #на главной странице
        response1 = self.client.get('/')
        self.assertContains(response1, text = 'test string 4')
        # проверка на профиле
        response2 = self.client.get('/test_user_1/')
        self.assertContains(response2, text = 'test string 4')
        # проверка для страницы поста
        response3 = self.client.get(f'/test_user_1/{post_id}/')
        self.assertContains(response3, text = 'test string 4')

    def tearDown(self):
            print("End testing")