from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from common.views import TitleMixin


class OrderCreateView(TitleMixin, TemplateView):
    template_name = 'orders/order-create.html'
    title = 'Store - Оформление заказа'


class OrderListView(TitleMixin, TemplateView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'


class OrderDetailView(TitleMixin, TemplateView):
    template_name = 'orders/order.html'
    title = 'Store - Заказ №12345'
