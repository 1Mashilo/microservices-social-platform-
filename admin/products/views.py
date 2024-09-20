from random import choice
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ProductSerializer
from .models import Product, User
from django.http import HttpResponse
from .producer import publish

# Simple view to return 'hello world'
def index(request):
    """
    A basic view function that returns a "hello world" response. This is likely a placeholder 
    or a test endpoint.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        HttpResponse: An HTTP response with the text "hello world".
    """
    return HttpResponse('hello world')

# ViewSet for handling CRUD operations on the Product model
class ProductViewSet(viewsets.ViewSet):
    """
    A ViewSet that provides CRUD (Create, Read, Update, Delete) operations for Product objects.
    """

    # Retrieve a list of all products
    def list(self, request):
        """
        Retrieves a list of all Product objects.

        Args:
            request (HttpRequest): The incoming HTTP request object.

        Returns:
            Response: A serialized list of all Product objects.
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # Create a new product
    def create(self, request):
        """
        Creates a new Product object.

        Args:
            request (HttpRequest): The incoming HTTP request object containing the product data.

        Returns:
            Response: The serialized representation of the newly created Product object, or an error response 
                      if the data is invalid.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product_created', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve details of a specific product
    def retrieve(self, request, pk=None):
        """
        Retrieves details of a specific Product object.

        Args:
            request (HttpRequest): The incoming HTTP request object.
            pk (int): The primary key (ID) of the Product object to retrieve.

        Returns:
            Response: The serialized representation of the Product object, or an error response 
                      if the product is not found.
        """
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # Update a specific product
    def update(self, request, pk=None):
        """
        Updates a specific Product object.

        Args:
            request (HttpRequest): The incoming HTTP request object containing the updated product data.
            pk (int): The primary key (ID) of the Product object to update.

        Returns:
            Response: The serialized representation of the updated Product object, or an error response 
                      if the product is not found or the data is invalid.
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

    # Delete a specific product
    def delete(self, request, pk=None):
        """
        Deletes a specific Product object.

        Args:
            request (HttpRequest): The incoming HTTP request object.
            pk (int): The primary key (ID) of the Product object to delete.

        Returns:
            Response: A 204 No Content response if the product is successfully deleted, or an error 
                      response if the product is not found.
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

        Args:
            request (HttpRequest): The incoming HTTP request object.

        Returns:
            Response: A JSON response containing the ID of a randomly selected User object.
        """
        users = User.objects.all()
        user = choice(users)
        return Response({'id': user.id})