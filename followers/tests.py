"""
This file contains API tests for the Followers endpoints.
It tests that a user can follow another user, cannot follow themselves,
and cannot follow the same user twice.
"""

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from followers.models import Follower

class FollowerAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create two users: one who will follow and one to be followed.
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")
        # Set the endpoint URL for followers as defined in followers/urls.py.
        self.follower_url = "/followers/"

    def test_follow_another_user(self):
        """
        Ensure that an authenticated user can follow another user.
        """
        self.client.login(username="user1", password="pass123")
        data = {"followed": self.user2.id}
        response = self.client.post(self.follower_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify that the 'owner' field in the response matches the logged-in user.
        self.assertEqual(response.data["owner"], "user1")
        # Verify that the 'followed' field matches the ID of the followed user.
        self.assertEqual(response.data["followed"], self.user2.id)

    def test_follow_self(self):
        """
        Ensure that a user cannot follow themselves.
        """
        self.client.login(username="user1", password="pass123")
        data = {"followed": self.user1.id}
        response = self.client.post(self.follower_url, data, format="json")
        # Expect a 400 Bad Request because following oneself is not allowed.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You cannot follow yourself", str(response.data))

    def test_duplicate_follow(self):
        """
        Ensure that a user cannot follow the same user twice.
        """
        self.client.login(username="user1", password="pass123")
        data = {"followed": self.user2.id}
        # First follow should succeed.
        response1 = self.client.post(self.follower_url, data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        # Second follow attempt should fail with a 400 error.
        response2 = self.client.post(self.follower_url, data, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You are already following", str(response2.data))

    def test_list_followers(self):
        """
        Ensure that the followers list endpoint returns the correct number of records.
        """
        self.client.login(username="user1", password="pass123")
        # First, user1 follows user2.
        data = {"followed": self.user2.id}
        self.client.post(self.follower_url, data, format="json")
        # Now, retrieve the list of followers.
        response = self.client.get(self.follower_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that at least one record is returned.
        self.assertTrue(len(response.data["results"]) >= 1)
