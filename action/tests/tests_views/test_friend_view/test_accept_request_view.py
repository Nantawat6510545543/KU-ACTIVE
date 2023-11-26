from django.urls import reverse
from django.contrib.messages import get_messages

from action.models import FriendStatus
from action.tests.utils import create_friend_status, FriendStatusViewSetup


class AcceptRequestViewTests(FriendStatusViewSetup):
    """Test cases for accepting friend requests."""

    def test_accept_not_friend(self):
        """
        Test whether users can accept requests from users who are not yet friended.

        Users should be redirected to the request view with a success message.
        """
        create_friend_status(self.user_1, self.user_2)  # no friend status

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
        Test whether users cannot accept requests from users who are already friends.

        Users should be redirected to the request view with a failed message.
        """
        create_friend_status(self.user_1, self.user_2, 'Accepted')  # already friend status

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
