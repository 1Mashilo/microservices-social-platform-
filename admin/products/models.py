from django.db import models

class Product(models.Model):
    """
    Model representing a product.

    Attributes:
        title (CharField): The title of the product.
        image (CharField): The URL or path to the product image.
        likes (PositiveIntegerField): The number of likes the product has.
    """

    title = models.CharField(max_length=200, help_text="Enter the title of the product")
    image = models.CharField(max_length=255, help_text="Enter the URL or path to the product image")
    likes = models.PositiveIntegerField(default=0, help_text="Number of likes for the product")

    def __str__(self):
        """
        String for representing the Product object.
        """
        return self.title

class User(models.Model):
    pass
