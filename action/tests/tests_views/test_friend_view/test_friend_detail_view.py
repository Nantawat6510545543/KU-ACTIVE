from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user


class ActivityStatusViewTests(TestCase):
    def setUp(self) -> None:
        user_data = {"email": "test@example.com"}
        self.user = create_user(username="John", password="abc", **user_data)

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
        self.client.force_login(self.user)
        response = self.client.get(reverse('action:friends'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('action:add_view'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('action:request_view'))
        self.assertEqual(response.status_code, 200)
