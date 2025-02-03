from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from comments.models import Comment
from posts.models import Post

class CommentAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user who will create the comment
        self.commenter = User.objects.create_user(username="testuser", password="testpass")
        # Create a user who owns the post
        self.post_owner = User.objects.create_user(username="postowner", password="testpass")
        # Create a sample post for commenting
        self.post = Post.objects.create(
            owner=self.post_owner,
            title="Test Post",
            content="Test Content",
            category="general"
        )
        # URL for the comments endpoint (as defined in comments/urls.py)
        self.comments_url = "/comments/"

    def test_create_comment_as_authenticated_user(self):
        """
        Ensure that an authenticated user can create a comment.
        """
        self.client.login(username="testuser", password="testpass")
        data = {
            "post": self.post.id,
            "content": "This is a test comment.",
            "category": "general"
        }
        response = self.client.post(self.comments_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "This is a test comment.")
        self.assertEqual(response.data["owner"], "testuser")

    def test_create_comment_as_anonymous_user(self):
        """
        Ensure that an anonymous (unauthenticated) user cannot create a comment.
        """
        data = {
            "post": self.post.id,
            "content": "Anonymous comment",
            "category": "general"
        }
        response = self.client.post(self.comments_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
