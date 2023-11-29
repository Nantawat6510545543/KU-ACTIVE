from django.test import TestCase
from action.models import FriendStatus
from action.utils import fetch_friend_status
from action.tests.utils import create_user, create_friend_status, create_request


class FriendStatusUtilsTestCase(TestCase):
    """Test case for the FriendStatus utility functions."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Set the view attribute to 'action:send_request'.
        2. Create two user instances, user1 and user2.
        """
        self.view = 'action:send_request'
        self.user1 = create_user(username='user1', password='password1')
        self.user2 = create_user(username='user2', password='password2')

    def test_user1_sender(self):
        """
        Test fetching FriendStatus when user1 is the sender.

        1. Create a request instance where user1 is the sender.
        2. Create a FriendStatus instance with request_status 'Accepted'.
        3. Call fetch_friend_status and assert the result is the created FriendStatus.
        """
        request = create_request(self.view, [self.user2.id], user=self.user1)
        friend_status = create_friend_status(self.user1, self.user2, request_status='Accepted')
        get_friend_status = fetch_friend_status(request, self.user2.id)
        self.assertEqual(get_friend_status, friend_status)

    def test_user1_receiver(self):
        """
        Test fetching FriendStatus when user1 is the receiver.

        1. Create a request instance where user1 is the receiver.
        2. Create a FriendStatus instance with request_status 'Accepted'.
        3. Call fetch_friend_status and assert the result is the created FriendStatus.
        """
        request = create_request(self.view, [self.user1.id], user=self.user2)
        friend_status = create_friend_status(self.user2, self.user1, request_status='Accepted')
        get_friend_status = fetch_friend_status(request, self.user1.id)
        self.assertEqual(get_friend_status, friend_status)

    def test_fetch_friend_status_not_existing(self):
        """
        Test fetching FriendStatus for a non-existing relationship.

        1. Create a request instance where user1 is the sender.
        2. Call fetch_friend_status for user2's id.
        3. Assert that the result is an instance of FriendStatus.
        """
        request = create_request(self.view, [self.user2.id], user=self.user1)
        get_friend_status = fetch_friend_status(request, self.user2.id)
        self.assertTrue(isinstance(get_friend_status, FriendStatus))
