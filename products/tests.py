from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Basket, Product, ProductCategory
from users.models import User


class IndexViewTestCase(TestCase):
    # названия функции всегда должны начинаться на test
    def test_view(self):
        # в тестах нужно имитировать работу пользователя
        path = reverse('index')
        response = self.client.get(path)  # делаем запрос на страницу

        # метод assertEqual позволяет убедиться, что фактический результат работы функции соответствует ожидаемому
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']  # использование наших fixtures

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


class BasketViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123')

    def test_add_to_basket(self):
        product = Product.objects.first()
        self.client.login(username='admin', password='123')
        path = reverse('products:basket_add', args=[product.id])
        response = self.client.post(path, HTTP_REFERER='/products/')

        self.assertEqual(Basket.objects.count(), 1)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, '/products/')

    def test_remove_from_basket(self):
        product = Product.objects.first()
        basket = Basket.objects.create(user=self.user, product=product)
        self.client.login(username='admin', password='123')
        path = reverse('products:basket_remove', args=[basket.id])
        response = self.client.post(path, HTTP_REFERER=f'/users/profile/{self.user.id}/')

        self.assertFalse(Basket.objects.filter(id=basket.id).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

