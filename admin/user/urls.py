from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import signup, user_login, ProfileViewSet


router = DefaultRouter()  

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('', include(router.urls)), 
]