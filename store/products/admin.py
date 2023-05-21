from django.contrib import admin

from products.models import Basket, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity',  'category')
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'stripe_product_price_id', 'category', 'slug')
    # readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('name',)
    # prepopulated_fields = {'slug': ('name',)} - автаматически заполняет слаг

class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0






