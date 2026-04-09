from http import HTTPStatus
from datetime import timedelta
from urllib import response

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import User, EmailVerification


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'first_name': 'Roma',
            'last_name': 'Sashyn',
            'username': 'roma',
            'email': 'roma@mail.ru',
            'password1': '123456@tT',
            'password2': '123456@tT',
        }

    # проверка на отображение формы(get запрос)
    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')

    # проверка на post запрос
    def test_user_registration_post_success(self):
        username = self.data['username']  # нужно для проверки пользователя
        self.assertFalse(User.objects.filter(username=username).exists())  # проверка вдруг пользователь уже есть
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # метод проверяющий успешное перенаправление
        # self.assertRedirects(response, reverse('users:login'))
        # метод проверяющий вернулось ли значение True
        self.assertTrue(User.objects.filter(username=username).exists())  # проверка создался ли пользователь

        # проверка создания EmailVerification объекта
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        # проверка правильного создания expiration по дате так как без этого будет ошибка
        self.assertEqual(
            email_verification.first().expiration.date(), (now() + timedelta(hours=48)).date()
        )

    # проверка на ошибки если username уже существует(отдельно надо сделать не валидный пароль и почта)
    def test_user_registration_post_username_error(self):
        User.objects.create(username=self.data['username'])  # создаем пользователя
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # так как произойдет ошибка мы останемся на той же странице
        # метод проверяющий сообщение на странице
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)

    def test_user_registration_post_email_error(self):
        data = {
            'first_name': 'Roma',
            'last_name': 'Sashyn',
            'username': 'roma',
            'email': 'romamail.ru',
            'password1': '123456@tT',
            'password2': '123456@tT',
        }
        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    # и так для каждого случая с паролем
    def test_user_registration_post_password_error(self):
        data = {
            'first_name': 'Roma',
            'last_name': 'Sashyn',
            'username': 'roma',
            'email': 'roma@mail.ru',
            'password1': '12345678',
            'password2': '12345678',
        }
        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введённый пароль слишком широко распространён.', html=True)
        self.assertContains(response, 'Введённый пароль состоит только из цифр.', html=True)
