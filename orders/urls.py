from django.urls import path

from orders.views import OrderCreateView, OrderListView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('all/', OrderListView.as_view(), name='order_list'),
    # path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order_detail/', OrderDetailView.as_view(), name='order_detail'),
]