from django.contrib import admin

from .models import ProductCategory, Product

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category')
    search_fields = ('name', 'description',)
    list_filter = ('category',)
