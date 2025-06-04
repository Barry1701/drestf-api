"""
API tests for the DirectMessage endpoints.
"""

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class DirectMessageAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.sender = User.objects.create_user(
            username="sender", password="pass123"
        )
        self.receiver = User.objects.create_user(
            username="receiver", password="pass123"
        )
        self.inbox_url = "/inbox/"

    def test_create_message_with_username_receiver(self):
        """Ensure that a direct message can be sent using the receiver's username."""
        self.client.login(username="sender", password="pass123")
        data = {
            "receiver": "receiver",
            "subject": "Test",
            "content": "Hello",
        }
        response = self.client.post(self.inbox_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["sender_username"], "sender")
        self.assertEqual(response.data["receiver"], "receiver")
        self.assertEqual(response.data["receiver_username"], "receiver")
