from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

client = stripe.StripeClient(settings.STRIPE_SECRET_KEY)
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


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
        # формируем список словарей с корзиной с фильтрацией по пользователю который отправляет запрос
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = client.v1.checkout.sessions.create(params={
            'line_items': baskets.stripe_products(),
            'metadata': {'order_id': self.object.id},  # нужно передать id для будущего использования
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
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = client.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print("Invalid payload:", e)
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        print("Signature verification failed:", e)
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        fulfill_order(session)

    return HttpResponse(status=HTTPStatus.OK)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)  # приходит в строковом типе, берется из metadata в checkout_session
    order = Order.objects.get(id=order_id)
    order.update_after_payment()


class OrderListView(TitleMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    ordering = ('-created',)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - {self.object.id}'
        return context