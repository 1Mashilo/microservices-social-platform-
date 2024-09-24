from random import choice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from django.http import HttpResponse
from django.contrib.auth.models import User
from .serializers import ProductSerializer, UserSerializer
from .models import Product
from .producer import publish

# Simple view to return 'hello world'
def index(request):
    """
    A basic view function that returns a "hello world" response.
    """
    return HttpResponse('hello world')

# ViewSet for handling CRUD operations on the Product model
class ProductViewSet(viewsets.ViewSet):
    """
    A ViewSet that provides CRUD operations for Product objects.
    """

    def list(self, request):
        """
        Retrieves a list of all Product objects.
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Creates a new Product object.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product_created', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieves details of a specific Product object.
        """
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Updates a specific Product object.
        """
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product_updated', serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Deletes a specific Product object.
        """
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

# APIView to retrieve a random User ID
class UserAPIView(APIView):
    """
    An APIView that retrieves a random User ID.
    """

    def get(self, request):
        """
        Handles GET requests to retrieve a random User ID.
        """
        users = User.objects.all()
        user = choice(users)
        return Response({'id': user.id})

# APIView to handle user registration
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
