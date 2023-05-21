import stripe
from django.conf import settings
from django.db import models
from django.utils.text import slugify

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'ProductCategory'


    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Product'

    def save(self , *args , **kwargs):
        self.slug = slugify(self.product_name)
        super(Product ,self).save(*args , **kwargs)


    def __str__(self):
        return f'Product: {self.name} | Category {self.category}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save( force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(int(self.price * 100)), currency='usd')
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Basket for {self.user.username} | Product: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity


    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item







