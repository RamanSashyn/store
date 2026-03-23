from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from products.models import ProductCategory, Product, Basket


class IndexView(TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = self.title
        return context


class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    # пагинация который заложен в ListView поэтому не надо объявлять классы и т.д(не надо настраивать вручную), но надо изменить шаблон

    def get_queryset(self):  # метод для фильтрации списка
        queryset = super(ProductsListView, self).get_queryset()
        # основной метод с чистым списком объектов т.е. Product.objects.all()
        category_id = self.kwargs.get('category_id')
        # достаем category_id из словаря поэтому через get чтобы не было ошибки
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data() # основной метод
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context


# def products(request, category_id=None, page_number=1):
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Store - Каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#     }
#     return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(product=product, user=request.user)

    if not baskets.exists():
        Basket.objects.create(product=product, user=request.user, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])