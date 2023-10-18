from django.test import TestCase
from action.models import User,FriendStatus


class FriendStatusTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender", password="testpassword")
        self.receiver = User.objects.create_user(
            username="receiver", password="testpassword")
        self.friend_status = FriendStatus.objects.create(
            sender=self.sender, receiver=self.receiver)

    def test_friend_status_sender(self):
        self.assertEqual(self.friend_status.sender, self.sender)

    def test_friend_status_receiver(self):
        self.assertEqual(self.friend_status.receiver, self.receiver)

    def test_friend_status_request_status_default(self):
        self.assertIsNone(self.friend_status.request_status)

    def test_friend_status_is_friend_default(self):
        self.assertFalse(self.friend_status.is_friend)

    def test_friend_status_request_status(self):
        self.friend_status.request_status = "Accepted"
        self.assertEqual(self.friend_status.request_status, "Accepted")

    def test_friend_status_is_friend(self):
        self.friend_status.is_friend = True
        self.assertTrue(self.friend_status.is_friend)
