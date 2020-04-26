from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post

User = get_user_model()


class PostsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test_user@test.ru', password='testpass1')

    #После регистрации пользователя создается его персональная страница (profile)
    def test_profile(self):
        response = self.client.get('/test_user/')
        self.assertEqual(response.status_code, 200)

    #Авторизованный пользователь может опубликовать пост (new)
    def test_logged_in(self):
        self.client.login(username='test_user', password='testpass1')
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)

    #Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/')

    #После публикации поста новая запись появляется на главной странице сайта (index), на персональной странице пользователя (profile), и на отдельной странице поста (post)
    def test_post(self):
        post = Post.objects.create(author=self.user, text='this is test post')

        for url in ('', '/test_user/', f'/test_user/{post.id}/'):
            response = self.client.get(url)
            self.assertContains(response, post.text)

    #Авторизованный пользователь может отредактировать свой пост и его содержимое изменится на всех связанных страницах
    def test_edit_post(self):
        self.client.login(username='test_user', password='testpass1')
        post = Post.objects.create(author=self.user, text='this is test post')
        response_edit = self.client.get(f'/test_user/{post.id}/edit/')
        self.assertEqual(response_edit.status_code, 200)
        post.text = 'This is edited test post'
        post.save()
        for url in ('', '/test_user/', f'/test_user/{post.id}/'):
            response = self.client.get(url)
            self.assertContains(response, post.text)



