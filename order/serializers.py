from rest_framework import serializers
from .models import Cart, CartItem, Order
from product.models import Product
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

    def create(self, validated_data):
        product = validated_data.pop('product_id')
        cart_id = self.context['cart_id']
        return CartItem.objects.create(cart_id=cart_id, product=product, **validated_data)

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status']
        read_only_fields = ['payment_status']