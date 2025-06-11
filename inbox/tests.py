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

    def test_receiver_can_mark_message_as_read(self):
        """Recipient should be able to mark a message as read."""
        self.client.login(username="sender", password="pass123")
        data = {
            "receiver": "receiver",
            "subject": "Test",
            "content": "Hello",
        }
        create_resp = self.client.post(self.inbox_url, data, format="json")
        msg_id = create_resp.data["id"]
        self.client.logout()

        self.client.login(username="receiver", password="pass123")
        patch_resp = self.client.patch(
            f"/messages/{msg_id}/",
            {"read": True},
            format="json",
        )
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(patch_resp.data["read"])

    def test_message_marked_as_read_on_retrieve(self):
        """Retrieving a message as the recipient should mark it as read."""
        self.client.login(username="sender", password="pass123")
        data = {
            "receiver": "receiver",
            "subject": "Test",
            "content": "Hello",
        }
        create_resp = self.client.post(self.inbox_url, data, format="json")
        msg_id = create_resp.data["id"]
        self.client.logout()

        self.client.login(username="receiver", password="pass123")
        get_resp = self.client.get(f"/messages/{msg_id}/", format="json")
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(get_resp.data["read"])

    def test_sender_retrieve_does_not_mark_read(self):
        """Retrieving a sent message should not change its read status."""
        self.client.login(username="sender", password="pass123")
        data = {
            "receiver": "receiver",
            "subject": "Test",
            "content": "Hello",
        }
        create_resp = self.client.post(self.inbox_url, data, format="json")
        msg_id = create_resp.data["id"]

        get_resp = self.client.get(f"/messages/{msg_id}/", format="json")
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)
        self.assertFalse(get_resp.data["read"])
