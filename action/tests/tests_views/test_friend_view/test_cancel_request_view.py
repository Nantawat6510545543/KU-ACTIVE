from django.urls import reverse
from django.contrib.messages import get_messages

from action.models import FriendStatus
from action.tests.utils import create_friend_status, FriendStatusViewSetup


class CancelRequestViewTests(FriendStatusViewSetup):
    """Test cases for canceling friend requests."""

    def test_cancel_request(self):
        """
        Test whether users can cancel pending friend requests.

        Users should be redirected to the add view with a success message.
        """
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
        """
        Test cases for invalid cancel requests.

        - User2 attempting to cancel User1's request.
        - User2 attempting to cancel their own request.

        Users should be redirected to the add_view with corresponding failed messages.
        """
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
