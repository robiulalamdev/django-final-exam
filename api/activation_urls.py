from django.urls import path
from djoser import views

urlpatterns = [
    path('activate/<str:uid>/<str:token>/', views.UserActivationView.as_view(), name='activate-user'),
]