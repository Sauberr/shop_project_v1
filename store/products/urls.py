
from django.urls import path

from products.views import (BasketView, ProductsListView, basket_add,
                            basket_remove, get_full_page_product)

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='home'),
    path('basket/', BasketView.as_view(), name='baskets'),
    path('<slug:slug>/', get_full_page_product, name="get_full_page_product"),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/category/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]

