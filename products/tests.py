from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):
    # названия функции всегда должны начинаться на test
    def test_view(self):
        # в тестах нужно имитировать работу пользователя
        path = reverse('index')
        response = self.client.get(path) # делаем запрос на страницу

        # метод assertEqual позволяет убедиться, что фактический результат работы функции или метода соответствует ожидаемому значению
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')