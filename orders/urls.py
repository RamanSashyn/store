from django.urls import path

from orders.views import (
    OrderCreateView, OrderListView, OrderDetailView, SuccessTemplateView, CanceledTemplateView)

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name='orders_list'),
    # path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order_detail/', OrderDetailView.as_view(), name='order_detail'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]