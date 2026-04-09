from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    # названия функции всегда должны начинаться на test
    def test_view(self):
        # в тестах нужно имитировать работу пользователя
        path = reverse('index')
        response = self.client.get(path) # делаем запрос на страницу

        # метод assertEqual позволяет убедиться, что фактический результат работы функции или метода соответствует ожидаемому значению
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json'] # использование наших fixtures

    # метод который позволяет объявить переменную которая будет использоваться в тестах
    def setUp(self):
        self.products = Product.objects.all()

    # проверяем выдаются ли товары на странице
    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))
        # так как на странице пагинация с 3 объектами нужен срез чтобы не было 6 объектов
        # даже если queryset опотбражает одинаковые данные они не будут между собой равны, поэтому переводим в list

    # проверяем фильтрацию товаров по категории
    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        # обязательно должнен передаваться id как в products/urls.py
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    # вынести общие проверки в отдельную функцию
    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], 'Store - Каталог')

