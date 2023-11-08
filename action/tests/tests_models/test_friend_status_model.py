from django.test import TestCase
from action.tests import utils


class FriendStatusTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.sender = utils.create_user(username="sender")
        self.receiver_list = [utils.create_user(f'receiver{i}') for i in
                              range(1, 5)]

        receiver_statuses = {
            self.receiver_list[0]: None,
            self.receiver_list[1]: 'Unknown',
            self.receiver_list[2]: 'Pending',
            self.receiver_list[3]: 'Accepted'
        }

        self.friend_status_list = [
            utils.create_friend_status(sender=self.sender, receiver=receiver,
                                       request_status=status)
            for receiver, status in receiver_statuses.items()
        ]

    def test_friend_status_attributes(self):
        statuses_check = {
            self.receiver_list[0]: (None, False),
            self.receiver_list[1]: (None, False),
            self.receiver_list[2]: ('Pending', False),
            self.receiver_list[3]: ('Accepted', True)
        }

        for status, (expected_request_status, expected_is_friend) in zip(
                self.friend_status_list, statuses_check.values()):
            self.assertEqual(status.sender, self.sender)
            self.assertIn(status.receiver, self.receiver_list)
            self.assertEqual(status.request_status, expected_request_status)
            self.assertEqual(status.is_friend, expected_is_friend)
