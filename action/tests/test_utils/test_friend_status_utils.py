from django.test import TestCase
from action.models import FriendStatus
from action.utils import fetch_friend_status

from action.tests.utils import create_user, create_friend_status, \
    create_request


class FriendStatusUtilsTestCase(TestCase):
    def setUp(self):
        self.view = 'action:add_friend'
        self.user1 = create_user(username='user1', password='password1')
        self.user2 = create_user(username='user2', password='password2')

    def test_user1_sender(self):
        request = create_request(self.view, [self.user2.id], user=self.user1)
        friend_status = create_friend_status(self.user1, self.user2,
                                             request_status='Accepted')

        get_friend_status = fetch_friend_status(request, self.user2.id)
        self.assertEqual(get_friend_status, friend_status)

    def test_user1_receiver(self):
        request = create_request(self.view, [self.user1.id], user=self.user2)
        friend_status = create_friend_status(self.user2, self.user1,
                                             request_status='Accepted')

        get_friend_status = fetch_friend_status(request, self.user1.id)
        self.assertEqual(get_friend_status, friend_status)

    def test_fetch_friend_status_not_existing(self):
        request = create_request(self.view, [self.user2.id], user=self.user1)
        get_friend_status = fetch_friend_status(request, self.user2.id)
        self.assertTrue(isinstance(get_friend_status, FriendStatus))
