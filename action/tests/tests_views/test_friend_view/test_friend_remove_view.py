from django.urls import reverse
from django.contrib.messages import get_messages

from action.models import FriendStatus
from action.tests.utils import create_friend_status, FriendStatusViewSetup


class RemoveViewTests(FriendStatusViewSetup):
    """Test cases for a remove friend."""

    def test_remove_friend(self):
        """
        Ensure that users can successfully remove friends.

        After removal, users should be redirected to the friends page, and the friendship status
        should be updated accordingly. Success messages should be displayed.
        """
        create_friend_status(self.user_1, self.user_2, 'Accepted')  # already friend status

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
        Ensure that users cannot remove users who are not friends.

        Users should be redirected to the friends page, and no changes should be made to the friendship status.
        Failure messages should be displayed.
        """
        create_friend_status(self.user_1, self.user_2)  # no friend status

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
