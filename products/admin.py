from django.contrib import admin

from .models import ProductCategory, Product

@admin.register(ProductCategory)
class ProductCategory(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Product)
class Category(admin.ModelAdmin):
    search_fields = ('name',)
