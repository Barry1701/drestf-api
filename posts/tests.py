"""
This file contains API tests for the Posts endpoints.
It tests listing, creating, updating, and deleting posts.
"""

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from posts.models import Post

class PostAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create two users: one who owns the post and another as a non-owner.
        self.owner = User.objects.create_user(username="poster", password="pass123")
        self.non_owner = User.objects.create_user(username="other", password="pass123")
        # Create a sample post owned by 'poster'
        self.post = Post.objects.create(
            owner=self.owner,
            title="First Post",
            content="Content of first post",
            category="general"
        )
        # Endpoint URLs for posts (assuming they are defined in posts/urls.py)
        self.posts_url = "/posts/"
        self.post_detail_url = f"/posts/{self.post.id}/"

    def test_list_posts(self):
        """
        Ensure that the post list endpoint returns posts with annotated fields.
        """
        response = self.client.get(self.posts_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that at least one post is returned.
        self.assertTrue(len(response.data["results"]) >= 1)
        # Check that the annotated fields 'likes_count' and 'comments_count' are present.
        post_data = response.data["results"][0]
        self.assertIn("likes_count", post_data)
        self.assertIn("comments_count", post_data)

    def test_create_post_authenticated(self):
        """
        Ensure that an authenticated user can create a post.
        """
        self.client.login(username="poster", password="pass123")
        data = {
            "title": "New Post",
            "content": "This is a new post",
            "category": "eczema"
        }
        response = self.client.post(self.posts_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Post")
        self.assertEqual(response.data["owner"], "poster")

    def test_update_post_as_owner(self):
        """
        Ensure that the owner can update their post.
        """
        self.client.login(username="poster", password="pass123")
        data = {
            "title": "Updated Post Title",
            "content": "Updated content",
            "category": "allergy"
        }
        response = self.client.put(self.post_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Post Title")

    def test_update_post_as_non_owner(self):
        """
        Ensure that a non-owner cannot update the post.
        """
        self.client.login(username="other", password="pass123")
        data = {
            "title": "Hacked Title",
            "content": "Hacked content",
            "category": "general"
        }
        response = self.client.put(self.post_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_as_owner(self):
        """
        Ensure that the owner can delete their post.
        """
        self.client.login(username="poster", password="pass123")
        response = self.client.delete(self.post_detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify that the post no longer exists.
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_post_as_non_owner(self):
        """
        Ensure that a non-owner cannot delete the post.
        """
        self.client.login(username="other", password="pass123")
        response = self.client.delete(self.post_detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
