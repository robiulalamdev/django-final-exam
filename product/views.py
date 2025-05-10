from product.models import Product, Category, Review, ProductImage, Wishlist
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer, WishlistSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from product.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from product.permissions import IsReviewAuthorOrReadonly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(tags=['Products'], operation_summary='Get latest 10 products')
    def latest(self, request):
        from rest_framework.response import Response
        latest_products = Product.objects.all().order_by('-created_at')[:8]
        serializer = self.get_serializer(latest_products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Products'], operation_summary='Retrieve a list of products')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Products'],
        operation_summary="Create a product by admin",
        operation_description="This allows an admin to create a product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Products'], operation_summary='Retrieve a specific product')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Products'], operation_summary='Update a product')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Products'], operation_summary='Partially update a product')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Products'], operation_summary='Delete a product')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))

    @swagger_auto_schema(tags=['Product Images'], operation_summary='List product images')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Product Images'], operation_summary='Add product image')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Product Images'], operation_summary='Get product image')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Product Images'], operation_summary='Update product image')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Product Images'], operation_summary='Partially update product image')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Product Images'], operation_summary='Delete product image')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(tags=['Categories'], operation_summary='List all categories')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Categories'], operation_summary='Create a category')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Categories'], operation_summary='Get category details')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Categories'], operation_summary='Update a category')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Categories'], operation_summary='Partially update a category')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Categories'], operation_summary='Delete a category')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(tags=['Reviews'], operation_summary='Get my reviews')
    def my_reviews(self, request):
        from rest_framework.response import Response
        reviews = Review.objects.filter(user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Reviews'], operation_summary='List product reviews')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Reviews'], operation_summary='Create a review')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Reviews'], operation_summary='Get review details')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Reviews'], operation_summary='Update a review')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Reviews'], operation_summary='Partially update a review')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Reviews'], operation_summary='Delete a review')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        product_pk = self.kwargs.get('product_pk')
        if product_pk is not None:
            queryset = Review.objects.filter(product_id=product_pk)
        else:
            queryset = Review.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}


class WishlistViewSet(ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['Wishlist'], operation_summary="List user's wishlist items")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Wishlist'], operation_summary='Add product to wishlist', request_body=WishlistSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Wishlist'], operation_summary='Get wishlist item details')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Wishlist'], operation_summary='Update wishlist item')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Wishlist'], operation_summary='Partially update wishlist item')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Wishlist'], operation_summary='Remove product from wishlist')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}
