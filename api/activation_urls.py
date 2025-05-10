from django.urls import path
from djoser.views import UserViewSet
from api.views import CustomActivationView

urlpatterns = [
    # path('activate/<str:uid>/<str:token>/', UserViewSet.as_view({'post': 'activation'}), name='activate-user'),
     path('activate/<str:uid>/<str:token>/', CustomActivationView.as_view(), name='activate-user'),
]