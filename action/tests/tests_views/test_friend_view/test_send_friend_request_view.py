from django.urls import reverse
from django.contrib.messages import get_messages

from action.models import FriendStatus
from action.tests.utils import create_friend_status, FriendStatusViewSetup


class SendRequestViewTests(FriendStatusViewSetup):
    """Test cases for sending friend request."""

    def test_send_request_new_friend(self):
        """
        Test whether users can send friend requests to other users successfully.

        Users should be redirected to the add_view with a success message,
        and the friend status should be set to 'Pending'.
        """
        create_friend_status(self.user_1, self.user_2)  # no friend status

        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:send_request', args=[self.user_2.id]))
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

    def test_send_request_current_friend(self):
        """
        Test whether users cannot send friend requests to those who are already friends.

        Users should be redirected to the add_view with a corresponding failed message,
        and the friend status should remain as 'Accepted'.
        """
        create_friend_status(self.user_1, self.user_2, 'Accepted')  # already friend status

        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:send_request', args=[self.user_2.id]))
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
