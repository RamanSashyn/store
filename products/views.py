from django.shortcuts import render


def index(request):
    context = {
        'title': 'Store',
        'is_promotion': False,
    }
    return render(request, 'products/index.html', context)


def products(request):
    return render(request, 'products/products.html')
