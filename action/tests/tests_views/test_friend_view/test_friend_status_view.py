from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages

from action.models import FriendStatus
from action.tests.utils import create_friend_status, create_user


class FriendStatusViewTests(TestCase):
    def setUp(self) -> None:
        user_data_1 = {"email": "test1@example.com"}
        user_data_2 = {"email": "test2@example.com"}
        self.user_1 = create_user(username="John", password="abc", **user_data_1)
        self.user_2 = create_user(username="Jane", password="abc", **user_data_2)

    def test_add_new_friend(self):
        """
        Should be able to send friend requests to other users.
        And the messages should be shown.
        """
        no_friend_status = create_friend_status(self.user_1, self.user_2)
        self.assertEqual(no_friend_status.request_status, None)
        self.assertFalse(no_friend_status.is_friend)

        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:add_friend', args=[self.user_2.id]))
        # Should be redirected.
        self.assertRedirects(response, reverse('action:add_view'))
        # Check the status again.
        friends_status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(friends_status.request_status, 'Pending')
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Request Sent.")

    def test_add_current_friend(self):
        """
        Should not be able to send friend requests to users who are already friends.
        Failed messages should be shown.
        """
        already_friend_status = create_friend_status(self.user_1, self.user_2, 'Accepted')
        self.assertEqual(already_friend_status.request_status, 'Accepted')
        self.assertTrue(already_friend_status.is_friend)

        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:add_friend', args=[self.user_2.id]))
        # Should be redirected.
        self.assertRedirects(response, reverse('action:add_view'))
        # Check the status again.
        friends_status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(friends_status.request_status, 'Accepted')
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are already friend with this person.")

    def test_remove_friend(self):
        """
        Should be able to remove friends.
        Success messages should be shown.
        """
        already_friend_status = create_friend_status(self.user_1, self.user_2, 'Accepted')
        self.assertEqual(already_friend_status.request_status, 'Accepted')
        self.assertTrue(already_friend_status.is_friend)

        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:remove_friend', args=[self.user_2.id]))
        # Should be redirected.
        self.assertRedirects(response, reverse('action:friends'))
        # Check the status again.
        friends_status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(friends_status.request_status, None)
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This person is no longer friend with you.")

    def test_remove_not_friend(self):
        """
        Should not be able to remove users who are not friend.
        Fail messages should be shown.
        """
        already_friend_status = create_friend_status(self.user_1, self.user_2, None)
        self.assertEqual(already_friend_status.request_status, None)
        self.assertFalse(already_friend_status.is_friend)

        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:remove_friend', args=[self.user_2.id]))
        # Should be redirected.
        self.assertRedirects(response, reverse('action:friends'))
        # Check the status again.
        friends_status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(friends_status.request_status, None)
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This person is not friend with you.")

    def test_accept_not_friend(self):
        """
        Should be able to accept requests from users who are not yet friend.
        success messages should be shown.
        """
        already_friend_status = create_friend_status(self.user_1, self.user_2, None)
        self.assertEqual(already_friend_status.request_status, None)
        self.assertFalse(already_friend_status.is_friend)

        self.client.force_login(self.user_2)
        response = self.client.get(reverse('action:accept_request', args=[self.user_1.id]))
        # Should be redirected.
        self.assertRedirects(response, reverse('action:request_view'))
        # Check the status again.
        friends_status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(friends_status.request_status, 'Accepted')
        self.assertTrue(friends_status.is_friend)
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are now friend with this person.")

    def test_accept_already_friend(self):
        """
        Should not be able to accept requests from users who are already friend.
        Failed messages should be shown.
        """
        already_friend_status = create_friend_status(self.user_1, self.user_2, 'Accepted')
        self.assertEqual(already_friend_status.request_status, 'Accepted')
        self.assertTrue(already_friend_status.is_friend)

        self.client.force_login(self.user_2)
        response = self.client.get(reverse('action:accept_request', args=[self.user_1.id]))
        # Should be redirected.
        self.assertRedirects(response, reverse('action:request_view'))
        # Check the status again.
        friends_status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(friends_status.request_status, 'Accepted')
        self.assertTrue(friends_status.is_friend)
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are already friend with this person.")

    def test_decline_not_friend(self):
        """
        Should be able to decline requests from users who are not yet friend.
        success messages should be shown.
        """
        already_friend_status = create_friend_status(self.user_1, self.user_2, None)
        self.assertEqual(already_friend_status.request_status, None)
        self.assertFalse(already_friend_status.is_friend)

        self.client.force_login(self.user_2)
        response = self.client.get(reverse('action:decline_request', args=[self.user_1.id]))
        # Should be redirected.
        self.assertRedirects(response, reverse('action:request_view'))
        # Check the status again.
        friends_status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(friends_status.request_status, 'Declined')
        self.assertFalse(friends_status.is_friend)
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have declined this person.")

    def test_decline_already_friend(self):
        """
        Should not be able to accept requests from users who are already friend.
        Failed messages should be shown.
        """
        already_friend_status = create_friend_status(self.user_1, self.user_2, 'Accepted')
        self.assertEqual(already_friend_status.request_status, 'Accepted')
        self.assertTrue(already_friend_status.is_friend)

        self.client.force_login(self.user_2)
        response = self.client.get(reverse('action:decline_request', args=[self.user_1.id]))
        # Should be redirected.
        self.assertRedirects(response, reverse('action:request_view'))
        # Check the status again.
        friends_status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(friends_status.request_status, 'Accepted')
        self.assertTrue(friends_status.is_friend)
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are already friend with this person.")
