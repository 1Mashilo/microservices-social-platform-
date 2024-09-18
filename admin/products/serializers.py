from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Meta class for ProductSerializer.

        Attributes:
            model (class): The model class to serialize.
            fields (list): The fields to include in the serialized output.
        """
        model = Product
        fields = '__all__'
