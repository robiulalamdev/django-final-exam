from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from order.models import Order, OrderItem
from product.models import Product, Review
from users.models import User
from datetime import datetime, timedelta

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_statistics(request):
    # Get date range for monthly data

    print('admin_statistics')
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Last 12 months
    
    # Monthly sales data
    monthly_sales = Order.objects.filter(
        placed_at__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('placed_at')
    ).values('month').annotate(
        total_sales=Sum('items__unit_price' * 'items__quantity'),
        order_count=Count('id')
    ).order_by('month')
    
    # Most popular products
    popular_products = Product.objects.annotate(
        total_ordered=Count('orderitem'),
        avg_rating=Avg('review__ratings')
    ).order_by('-total_ordered')[:10]
    
    # Top buyers
    top_buyers = User.objects.annotate(
        total_spent=Sum('order__items__unit_price' * 'order__items__quantity'),
        order_count=Count('order')
    ).exclude(total_spent=None).order_by('-total_spent')[:10]
    
    # Recent orders
    recent_orders = Order.objects.annotate(
        total_amount=Sum('items__unit_price' * 'items__quantity')
    ).select_related('user').order_by('-placed_at')[:5]
    
    return Response({
        'monthly_sales': [{
            'month': item['month'].strftime('%Y-%m'),
            'total_sales': float(item['total_sales']),
            'order_count': item['order_count']
        } for item in monthly_sales],
        'popular_products': [{
            'id': product.id,
            'name': product.name,
            'total_ordered': product.total_ordered,
            'avg_rating': float(product.avg_rating) if product.avg_rating else None
        } for product in popular_products],
        'top_buyers': [{
            'id': user.id,
            'email': user.email,
            'total_spent': float(user.total_spent),
            'order_count': user.order_count
        } for user in top_buyers],
        'recent_orders': [{
            'id': order.id,
            'user_email': order.user.email,
            'total_amount': float(order.total_amount),
            'created_at': order.created_at
        } for order in recent_orders]
    })