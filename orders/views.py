import stripe
from http import HTTPStatus

from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, DetailView, CreateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order

client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)
endpoint_secret = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/cancel.html'



class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = client.v1.checkout.sessions.create(params={
            'line_items': [
                {
                    'price': 'price_1TMVpE4DTPB8CBsAfAhN4LZj',
                    'quantity': 1,
                },
            ],
            'mode': 'payment',
            'success_url': '{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            'cancel_url': '{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        })
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body

    print(payload)

    return HttpResponse(status=HTTPStatus.OK)


class OrderListView(TitleMixin, TemplateView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'


class OrderDetailView(TitleMixin, TemplateView):
    template_name = 'orders/order.html'
    title = 'Store - Заказ №12345'
