from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Basket, Product, ProductCategory
from products.permissions import IsAdminOrReadOnly
from products.serializers import (BasketSerializer, ProductCategorySerializer,
                                  ProductSerializer)
from users.models import User
from users.serializers import UserSerializer


@method_decorator(login_required, name='dispatch')
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(ProductModelViewSet, self).get_permissions()


class ProductCategoryApiPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


# @method_decorator(login_required, name='dispatch'
class ProductCategoryModelViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = ProductCategoryApiPagination
    # authentication_classes = (TokenAuthentication,)

    # def get_permissions(self):
    #     if self.action in ('create', 'update', 'destroy'):
    #         self.permission_classes = (IsAdminUser,)
    #     return super(ProductModelViewSet, self).get_permissions()


@method_decorator(login_required, name='dispatch')
class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': 'There is no product with this ID.'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.create_or_update(products.first().id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product_id': 'Thi field is required.'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name='dispatch')
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
