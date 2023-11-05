from django.test import TestCase
from action.tests import utils


class FriendStatusTestCase(TestCase):
    def setUp(self):
        self.sender = utils.create_user(username="sender")
        self.receiver = utils.create_user(username="receiver")
        self.friend_status = utils.create_friend_status(sender=self.sender,
                                                        receiver=self.receiver)

    def test_friend_status_attributes(self):
        friend_status = self.friend_status

        self.assertEqual(friend_status.sender, self.sender)
        self.assertEqual(friend_status.receiver, self.receiver)
        self.assertIsNone(friend_status.request_status)
        self.assertFalse(friend_status.is_friend)
