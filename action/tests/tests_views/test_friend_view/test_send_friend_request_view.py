from django.urls import reverse
from django.contrib.messages import get_messages

from action.models import FriendStatus
from action.tests.end_to_end_base import EndToEndTestBase
from action.tests.utils import create_friend_status, create_user, FriendStatusViewSetup

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


class FriendRequestSendTestsE2E(EndToEndTestBase):
    """Test case for the views related to friends request."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Define 2 usernames and passwords.
        2. Create 2 users with the defined usernames and passwords.
        """
        super().setUp()
        self.name_1 = 'user1'
        self.password_1 = 'pass1'
        self.name_2 = 'user2'
        self.password_2 = 'pass2'
        self.user_1 = create_user(self.name_1, self.password_1)
        self.user_2 = create_user(self.name_2, self.password_2)

    def test_send_friend_request(self):
        """
        Test sending friend request to other user.

        1. LogIn as user_1.
        2. Navigate to the add friend page.
        3. Click add button.
        4. Check the friend request status.
        """
        # LogIn as user_1
        self.login(self.name_1, self.password_1)

        # Navigate to add friend page
        url = self.getUrl("action:add_view")
        self.browser.get(url)

        # Find user_2
        friend = self.find_by_class("each-friend")
        self.assertIn(self.user_2.username, friend.text)

        # Click add button
        add_button = self.find_by_class("add-button")
        self.assertEqual(add_button.text, "Add friend")
        add_button.click()

        # Check the messages
        message = self.find_by_class("alert-msg")
        self.assertIn("Request Sent.", message.text)

        # Check the cancel button
        cancel_button = self.find_by_class("cancel-button")
        self.assertEqual(cancel_button.text, "Cancel friend request")

        # Check the friend status
        status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(status.request_status, "Pending")

    def test_cancel_friend_request(self):
        """
        Test cancel friend request that sent to other user.

        1. LogIn as user_1.
        2. Navigate to the add friend page.
        3. Click add button.
        4. Click the cancel button.
        5. Check the friend request status.
        """
        # LogIn as user_1
        self.login(self.name_1, self.password_1)

        # Navigate to add friend view
        url = self.getUrl("action:add_view")
        self.browser.get(url)

        # Click add button
        add_button = self.find_by_class("add-button")
        self.assertEqual(add_button.text, "Add friend")
        add_button.click()

        # Click cancel button
        cancel_button = self.find_by_class("cancel-button")
        self.assertEqual(cancel_button.text, "Cancel friend request")
        cancel_button.click()

        # Check the messages
        message = self.find_by_class("alert-msg")
        self.assertIn("Request cancelled.", message.text)

        # Check the add button
        add_button = self.find_by_class("add-button")
        self.assertEqual(add_button.text, "Add friend")

        # Check the request status
        with self.assertRaises(FriendStatus.DoesNotExist):
            FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)

    def test_accept_friend_request(self):
        """
        Test accept friend request that from other user.

        1. LogIn as user_1.
        2. Navigate to the add friend page.
        3. Click add button.
        4. LogOut.
        5. LogIn as user_2.
        6. Navigate to the request friend page.
        7. Click accept the request.
        8. Check the friend request status.
        """
        # LogIn as user_1
        self.login(self.name_1, self.password_1)

        # Navigate to add friend page
        url = self.getUrl("action:add_view")
        self.browser.get(url)

        # Click add button
        add_button = self.find_by_class("add-button")
        add_button.click()

        # LogOut
        logout_button = self.find_by_class("logout")
        logout_button.click()

        # LogIn as user_2
        self.login(self.name_2, self.password_2)

        # Navigate to friend request page
        url = self.getUrl("action:request_view")
        self.browser.get(url)

        # Click accept friend request
        accept_button = self.find_by_class("accept-button")
        accept_button.click()

        # Check the messages
        message = self.find_by_class("alert-msg")
        self.assertIn("You are now friend with this person.", message.text)

        # Check the friend status
        status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertEqual(status.request_status, "Accepted")
        self.assertTrue(status.is_friend)

    def test_decline_friend_request(self):
        """
        Test decline friend request that from other user.

        1. LogIn as user_1.
        2. Navigate to the add friend page.
        3. Click add button.
        4. LogOut.
        5. LogIn as user_2.
        6. Navigate to the request friend page.
        7. Click decline the request.
        8. Check the friend request status.
        """
        # LogIn as user_1
        self.login(self.name_1, self.password_1)

        # Navigate to add friend page
        url = self.getUrl("action:add_view")
        self.browser.get(url)

        # Click add button
        add_button = self.find_by_class("add-button")
        add_button.click()

        # LogOut
        logout_button = self.find_by_class("logout")
        logout_button.click()

        # LogIn as user_2
        self.login(self.name_2, self.password_2)

        # Navigate to friend request page
        url = self.getUrl("action:request_view")
        self.browser.get(url)

        # Click decline friend request
        decline_button = self.find_by_class("decline-button")
        decline_button.click()

        # Check the messages
        message = self.find_by_class("alert-msg")
        self.assertIn("You have declined this person.", message.text)

        # Check the friend status
        with self.assertRaises(FriendStatus.DoesNotExist):
            FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)

    def test_delete_friend(self):
        """
        Test delete friend.

        1. LogIn as user_1.
        2. Navigate to the add friend page.
        3. Click add button.
        4. LogOut.
        5. LogIn as user_2.
        6. Navigate to the request friend page.
        7. Click accept the request.
        8. Navigate to friends page.
        9. Click remove friend.
        10. Check the messages.
        11. Check the friend status.
        """
        # LogIn as user_1
        self.login(self.name_1, self.password_1)

        # Navigate to add friend page
        url = self.getUrl("action:add_view")
        self.browser.get(url)

        # Click add button
        add_button = self.find_by_class("add-button")
        add_button.click()

        # LogOut
        logout_button = self.find_by_class("logout")
        logout_button.click()

        # LogIn as user_2
        self.login(self.name_2, self.password_2)

        # Navigate to friend request page
        url = self.getUrl("action:request_view")
        self.browser.get(url)

        # Click accept the request
        accept_button = self.find_by_class("accept-button")
        accept_button.click()

        # Navigate to friends page
        url = self.getUrl("action:friends")
        self.browser.get(url)

        # Click remove button
        add_button = self.find_by_class("remove-button")
        add_button.click()

        # Check the messages
        message = self.find_by_class("alert-msg")
        self.assertIn("This person is no longer friend with you.", message.text)

        # Check the friend status
        status = FriendStatus.objects.get(sender=self.user_1, receiver=self.user_2)
        self.assertIsNone(status.request_status)
        self.assertFalse(status.is_friend)
