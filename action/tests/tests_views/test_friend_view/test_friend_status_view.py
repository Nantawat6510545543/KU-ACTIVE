from abc import ABC
from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages

from action.models import FriendStatus
from action.tests.utils import create_friend_status, create_user, USER_DATA_1, USER_DATA_2


class FriendStatusViewSetup(ABC, TestCase):
    def setUp(self) -> None:
        self.user_1 = create_user(**USER_DATA_1)
        self.user_2 = create_user(**USER_DATA_2)


class AddViewTests(FriendStatusViewSetup):
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


class RemoveViewTests(FriendStatusViewSetup):
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


class AcceptRequestViewTests(FriendStatusViewSetup):
    def test_accept_not_friend(self):
        """
        Should be able to accept requests from users who are not yet friend.
        success messages should be shown.
        """
        already_friend_status = create_friend_status(self.user_1, self.user_2)
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


class DeclineRequestViewTests(FriendStatusViewSetup):
    def test_decline_not_friend(self):
        """
        Should be able to decline requests from users who are not yet friend.
        success messages should be shown.
        """
        already_friend_status = create_friend_status(self.user_1, self.user_2)
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


class CancelRequestViewTests(FriendStatusViewSetup):
    def test_cancel_request(self):
        friend_status = create_friend_status(self.user_1, self.user_2, 'Pending')

        # Case where user1 tries to cancel user2's request
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:cancel_request', args=[self.user_2.id]))
        self.assertRedirects(response, reverse('action:add_view'))
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)

        self.assertEqual(str(messages[0]), "Request cancelled.")

        with self.assertRaises(FriendStatus.DoesNotExist): 
            FriendStatus.objects.get(id=friend_status.id)

    def test_invalid_cancel_request(self):
        friends_status = create_friend_status(self.user_1, self.user_2, 'Pending')

        # Case where user2 tries to cancel user1's request
        self.client.force_login(self.user_2)
        response = self.client.get(reverse('action:cancel_request', args=[self.user_1.id]))
        self.assertRedirects(response, reverse('action:add_view'))
        # Check the messages.
        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(str(messages[0]), "There is no friend request for that person.")
        self.assertEqual(friends_status.request_status, 'Pending')

        # Case where user2 tries to cancel user2's request
        response = self.client.get(reverse('action:cancel_request', args=[self.user_2.id]))
        self.assertRedirects(response, reverse('action:add_view'))
        # Check the messages.
        storage = get_messages(response.wsgi_request)

        messages = list(storage)
        self.assertEqual(str(messages[0]), "There is no friend request for that person.")
        self.assertEqual(friends_status.request_status, 'Pending')
