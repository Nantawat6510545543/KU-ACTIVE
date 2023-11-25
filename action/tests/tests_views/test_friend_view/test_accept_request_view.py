from django.urls import reverse
from django.contrib.messages import get_messages

from action.models import FriendStatus
from action.tests.utils import create_friend_status, FriendStatusViewSetup


class AcceptRequestViewTests(FriendStatusViewSetup):
    def test_accept_not_friend(self):
        """
        Should be able to accept requests from users who are not yet friend.
        success messages should be shown.
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
        Should not be able to accept requests from users who are already friend.
        Failed messages should be shown.
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