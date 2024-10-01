from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    """
    Model representing a user profile on a social media platform.

    Attributes:
        user (ForeignKey): A one-to-one relationship with the User model, ensuring each user has one profile.
        id_user (IntegerField): An integer field storing the user's ID.
        bio (TextField): A text field for the user's biography (optional).
        profileimg (ImageField): An image field for the user's profile picture, with a default image provided.
        location (CharField): A character field for the user's location (optional).

    Methods:
        __str__: Returns the username of the associated user for easy representation.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    """
    Model representing a post on a social media platform.

    Attributes:
        id (UUIDField): A unique identifier for each post, automatically generated using UUID.
        user (CharField): The username of the user who created the post.
        image (ImageField): The image associated with the post.
        caption (TextField): The caption or description provided for the post.
        created_at (DateTimeField): The date and time when the post was created, defaults to the current datetime.
        no_of_likes (IntegerField): The number of likes the post has received, defaults to 0.

    Methods:
        __str__: Returns the username of the user who created the post for easy representation.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    """
    Model representing a like on a post.

    Attributes:
        post_id (CharField): The ID of the post that was liked.
        username (CharField): The username of the user who liked the post.

    Methods:
        __str__: Returns the username of the user who liked the post for easy representation.
    """

    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    """
    Model representing a follower relationship between users.

    Attributes:
        follower (CharField): The username of the follower.
        user (CharField): The username of the user being followed.

    Methods:
        __str__: Returns the username of the user being followed for easy representation.
    """

    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user