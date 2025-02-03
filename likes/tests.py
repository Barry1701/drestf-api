"""
This file contains API tests for the Likes endpoints.
It tests that an authenticated user can create a like, duplicate likes are prevented,
the list endpoint returns likes, and that a user can delete their own like.
"""

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from likes.models import Like
from posts.models import Post

class LikeAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user who will perform the like action.
        self.liker = User.objects.create_user(username="liker", password="pass123")
        # Create a user who owns the post.
        self.post_owner = User.objects.create_user(username="postowner", password="pass123")
        # Create a sample post.
        self.post = Post.objects.create(
            owner=self.post_owner,
            title="Test Post",
            content="Test Content",
            category="general"
        )
        # URL for the likes endpoint (as defined in likes/urls.py).
        self.like_url = "/likes/"

    def test_create_like_authenticated(self):
        """
        Ensure that an authenticated user can create a like.
        """
        self.client.login(username="liker", password="pass123")
        data = {"post": self.post.id}
        response = self.client.post(self.like_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["owner"], "liker")
        self.assertEqual(response.data["post"], self.post.id)

    def test_duplicate_like(self):
        """
        Ensure that a user cannot like the same post twice.
        """
        self.client.login(username="liker", password="pass123")
        data = {"post": self.post.id}
        # Create the first like.
        response1 = self.client.post(self.like_url, data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        # Attempt to create a duplicate like.
        response2 = self.client.post(self.like_url, data, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already liked", str(response2.data))

    def test_list_likes(self):
        """
        Ensure that the likes list endpoint returns the created likes.
        """
        self.client.login(username="liker", password="pass123")
        data = {"post": self.post.id}
        # Create a like.
        self.client.post(self.like_url, data, format="json")
        # Retrieve the list of likes.
        response = self.client.get(self.like_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that at least one like is returned.
        self.assertTrue(len(response.data["results"]) >= 1)

    def test_delete_like(self):
        """
        Ensure that a user can delete their own like.
        """
        self.client.login(username="liker", password="pass123")
        data = {"post": self.post.id}
        # Create a like.
        response_create = self.client.post(self.like_url, data, format="json")
        like_id = response_create.data["id"]
        # Delete the like using the detail endpoint.
        detail_url = f"/likes/{like_id}/"
        response_delete = self.client.delete(detail_url, format="json")
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        # Verify that the like no longer exists.
        self.assertFalse(Like.objects.filter(id=like_id).exists())

