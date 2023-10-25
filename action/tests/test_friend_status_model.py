from .utils import Tester


class FriendStatusTestCase(Tester):
    def setUp(self):
        self.sender = self.create_user(username="sender")
        self.receiver = self.create_user(username="receiver")
        self.friend_status = self.create_friend_status(sender=self.sender,
                                                       receiver=self.receiver)

    def test_friend_status_attributes(self):
        friend_status = self.friend_status

        self.assertEqual(friend_status.sender, self.sender)
        self.assertEqual(friend_status.receiver, self.receiver)
        self.assertIsNone(friend_status.request_status)
        self.assertFalse(friend_status.is_friend)
