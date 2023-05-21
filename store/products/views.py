from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class HomeView(TitleMixin, TemplateView):
    template_name = 'products/home.html'
    title = 'IGUS'

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data()
    #     context['title'] = 'Home'
    #     return context

# def home(request):
#     context = {
#         'title': 'Home',
#     }
#     return render(request, 'products/home.html', context)


class BasketView(TitleMixin, TemplateView):
    template_name = 'products/baskets.html'
    title = 'Basket'


# def basket(request):
#     return render(request, 'products/baskets.html')


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Clothes'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        # categories = cache.get('categories')
        # if not categories:
        #     context['categories'] = ProductCategory.objects.all()
        #     cache.set('categories', context['categories'], 30)
        # else:
        #     context['categories'] = categories

        # context['title'] = 'Clothes'
        context['categories'] = ProductCategory.objects.all()
        return context


# def products(request, category_id=None, page_number=1):
#
#     if category_id:
#         products = Product.objects.filter(category_id=category_id)
#     else:
#         products = Product.objects.all()
#
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#
#     per_page = 3
#     paginator = Paginator(products, per_page)
#
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Clothes',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#     }
#     return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
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


def get_full_page_product(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'products/product_page.html', context={'products': product, 'title': 'Full Product Page'})


