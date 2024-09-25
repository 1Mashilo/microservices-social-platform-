from django.urls import path
from .views import (
    register_user, login_user
)

urlpatterns = [
    path('products', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='product-list'),

    path('products/<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'delete',
    }), name='product-detail'),

    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),

    
]
