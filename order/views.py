from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(tags=['Cart'], operation_summary='List user\'s cart items')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart'], operation_summary='Create a new cart')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart'], operation_summary='Get cart details')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart'], operation_summary='Update cart')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart'], operation_summary='Partially update cart')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart'], operation_summary='Delete cart')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    @swagger_auto_schema(tags=['Cart Items'], operation_summary='List items in a cart')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart Items'], operation_summary='Add item to cart')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart Items'], operation_summary='Get cart item details')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart Items'], operation_summary='Update cart item')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart Items'], operation_summary='Partially update cart item')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Cart Items'], operation_summary='Remove item from cart')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class OrderViewset(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(tags=['Orders'], operation_summary='List user\'s orders')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Orders'], operation_summary='Create a new order')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Orders'], operation_summary='Get order details')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Orders'], operation_summary='Update order')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Orders'], operation_summary='Partially update order')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Orders'], operation_summary='Delete order')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)