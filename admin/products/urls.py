from django.urls import path
from .views import (
    ProductViewSet, loginView, registerView, index, logoutView, user, CookieTokenRefreshView
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

    path('login', loginView, name='login'),
    path('register', registerView, name='register'),
    path('refresh-token', CookieTokenRefreshView.as_view(), name='refresh-token'),
    path('logout', logoutView, name='logout'),
    path('user', user, name='user'),
]
