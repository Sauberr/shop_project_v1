from django.urls import path

from orders.views import (CanceledTemplateView, OrderCreateView, OrderListView,
                          SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessTemplateView.as_view(),  name='order-success'),
    path('order-canceled/', CanceledTemplateView.as_view(),  name='order-canceled'),
    path('', OrderListView.as_view(),  name='orders_list'),

]