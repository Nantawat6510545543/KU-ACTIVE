from django.urls import reverse
from django.contrib.messages import get_messages

from action.models import FriendStatus
from action.tests.utils import create_friend_status, FriendStatusViewSetup

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