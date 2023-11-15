from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user


class ProfileDetailViewTests(TestCase):
    def setUp(self) -> None:
        user_data_1 = {"email": "test1@example.com"}
        self.user_1 = create_user(username="John", password="abc", **user_data_1)
        user_data_2 = {"email": "test2@example.com"}
        self.user_2 = create_user(username="Jane", password="abc", **user_data_2)

    def test_guest_view_profile(self):
        """
        Guest should not be able to view their own profile.
        Should be redirected to Login page.
        """
        response = self.client.get(reverse('action:profile'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_view_profile(self):
        """
        Authenticated users should be able to view their own profile.
        """
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:profile'))
        self.assertEqual(response.status_code, 200)

    def test_guest_view_others_profile(self):
        """
        Guest should not be able to view others profile.
        Should be redirected.
        """
        response = self.client.get(reverse('action:profile'), args=(self.user_2.id,))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_view_others_profile(self):
        """
        Authenticated users should be able to view others profile.
        """
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:profile'), args=(self.user_2.id,))
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.user_2)
        response = self.client.get(reverse('action:profile'), args=(self.user_1.id,))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_view_own_profile(self):
        """
        Authenticated users should be able to view their own profile.
        """
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:profile'), args=(self.user_1.id,))
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.user_2)
        response = self.client.get(reverse('action:profile'), args=(self.user_2.id,))
        self.assertEqual(response.status_code, 200)
