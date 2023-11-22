from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user, create_friend_status


class ActivityStatusViewTests(TestCase):
    def setUp(self) -> None:
        user_data_1 = {"email": "test1@example.com"}
        user_data_2 = {"email": "test2@example.com"}
        self.user_1 = create_user(username="John", password="abc", **user_data_1)
        self.user_2 = create_user(username="Jane", password="abc", **user_data_2)

    def test_friend_view_guest(self):
        """
        Guest should not be able to view any friends page.
        Should be redirected.
        """
        response = self.client.get(reverse('action:friends'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('action:add_view'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('action:request_view'))
        self.assertEqual(response.status_code, 302)

    def test_friend_view_authenticated(self):
        """
        Authenticated users should be able to view all friends pages.
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
        If the users have friends, Query should be able to show their friends.
        """
        create_friend_status(self.user_1, self.user_2, 'Accepted')
        self.client.force_login(self.user_1)
        url = reverse('action:friends') + f'?q={self.user_2.username}'
        response = self.client.get(url)
        self.assertContains(response, self.user_2.username)

    def test_friend_add_query(self):
        """
        The query should work if the user is not already friends
        with the user they are searching for.
        """
        create_friend_status(self.user_1, self.user_2)
        self.client.force_login(self.user_1)
        url = reverse('action:add_view') + f'?q={self.user_2.username}'
        response = self.client.get(url)
        self.assertContains(response, self.user_2.username)

    def test_friend_request_query(self):
        """
        If the users have friend requests, Query should be able to show their friend requests.
        """
        create_friend_status(self.user_2, self.user_1, 'Pending')
        self.client.force_login(self.user_1)
        url = reverse('action:request_view') + f'?q={self.user_2.username}'
        response = self.client.get(url)
        self.assertContains(response, self.user_2.username)
