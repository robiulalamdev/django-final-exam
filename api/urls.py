from django.urls import path, include
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet, ProductImageViewSet, WishlistViewSet
from order.views import CartViewSet, CartItemViewSet, OrderViewset
from rest_framework_nested import routers
from .admin_views import admin_statistics

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewset, basename='orders')
router.register('wishlist', WishlistViewSet, basename='wishlist')

product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')
product_router.register('images', ProductImageViewSet,
                        basename='product-images')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('admin/statistics/', admin_statistics, name='admin-statistics'),
]
