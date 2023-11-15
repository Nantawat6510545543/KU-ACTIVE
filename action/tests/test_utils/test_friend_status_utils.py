from django.test import RequestFactory, TestCase
from django.urls import reverse
from action.models import FriendStatus
from action.utils import fetch_friend_status

from action.tests import utils


class FriendStatusUtilsTestCase(TestCase):
    def setUp(self):
        self.user1 = utils.create_user(username='user1', password='password1')
        self.user2 = utils.create_user(username='user2', password='password2')

        self.request = RequestFactory().get(reverse('action:add_friend',
                                                    args=[self.user2.id]))
        self.request.user = self.user1

    def test_fetch_friend_status_existing(self):
        # Create an existing friend status
        friend_status = utils.create_friend_status(self.user1, self.user2,
                                                   request_status='Accepted')

        get_friend_status = fetch_friend_status(self.request, self.user2.id)
        self.assertEqual(get_friend_status, friend_status)

    def test_fetch_friend_status_not_existing(self):
        get_friend_status = fetch_friend_status(self.request, self.user2.id)
        self.assertTrue(isinstance(get_friend_status, FriendStatus))
