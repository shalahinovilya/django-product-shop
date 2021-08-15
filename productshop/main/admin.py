from django.contrib import admin
from . models import Product, Category, Cart, CartProduct, Order


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'title', 'slug', 'content', 'price', 'img', 'cat')
    list_editable = ('content', 'price', 'cat', 'img')
    list_display_links = ('id', )
    search_fields = ('cat',)
    list_filter = ('cat',)
    save_on_top = True


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)