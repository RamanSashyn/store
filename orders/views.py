from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, CreateView
from django.urls import reverse_lazy

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class OrderListView(TitleMixin, TemplateView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'


class OrderDetailView(TitleMixin, TemplateView):
    template_name = 'orders/order.html'
    title = 'Store - Заказ №12345'
