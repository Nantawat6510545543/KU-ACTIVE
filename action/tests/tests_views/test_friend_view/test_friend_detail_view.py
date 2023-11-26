from django.urls import reverse
from action.tests.utils import create_friend_status, FriendStatusViewSetup


class DetailViewTest(FriendStatusViewSetup):
    """Test cases for view friend page."""

    def test_friend_view_guest(self):
        """
        Ensure that guests cannot view any friend-related pages.

        Guests should be redirected to the login page.
        """
        response = self.client.get(reverse('action:friends'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('action:add_view'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('action:request_view'))
        self.assertEqual(response.status_code, 302)

    def test_friend_view_authenticated(self):
        """
        Ensure that authenticated users can view all friend-related pages.

        Authenticated users should be able to access friends, add friends, and view friend requests pages.
        """
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:friends'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('action:add_view'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('action:request_view'))
        self.assertEqual(response.status_code, 200)

    def test_friend_list_query(self):
        """
        Ensure that the friend list query displays the correct results when users have friends.

        Users should be able to see their friends in the friend list based on the search query.
        """
        create_friend_status(self.user_1, self.user_2, 'Accepted')
        self.client.force_login(self.user_1)
        url = reverse('action:friends') + f'?q={self.user_2.username}'
        response = self.client.get(url)
        self.assertContains(response, self.user_2.username)

    def test_friend_add_query(self):
        """
        Ensure that the add friend query works when the user is not already friends with the searched user.

        Users should be able to see the searched user in the add friend view based on the search query.
        """
        create_friend_status(self.user_1, self.user_2)
        self.client.force_login(self.user_1)
        url = reverse('action:add_view') + f'?q={self.user_2.username}'
        response = self.client.get(url)
        self.assertContains(response, self.user_2.username)

    def test_friend_request_query(self):
        """
        Ensure that the friend request query displays the correct results when users have friend requests.

        Users should be able to see their friend requests in the friend request view based on the search query.
        """
        create_friend_status(self.user_2, self.user_1, 'Pending')
        self.client.force_login(self.user_1)
        url = reverse('action:request_view') + f'?q={self.user_2.username}'
        response = self.client.get(url)
        self.assertContains(response, self.user_2.username)
