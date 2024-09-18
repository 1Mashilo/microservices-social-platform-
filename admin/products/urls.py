from django.urls import path
from .views import ProductViewSet, UserAPIView, index

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

    path('user', UserAPIView.as_view(), name='user-list'),
    path('index', index, name='index'),
]
