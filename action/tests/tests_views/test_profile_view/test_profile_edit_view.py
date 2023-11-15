from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user


class ProfileEditViewTests(TestCase):
    def setUp(self) -> None:
        user_data_1 = {"email": "test1@example.com"}
        self.user_1 = create_user(username="John", password="abc", **user_data_1)
        # user_data_2 = {"email": "test2@example.com"}
        # self.user_2 = create_user(username="Jane", password="abc", **user_data_2)

    def test_guest_view_profile_edit(self):
        """
        Guest should not be able to edit their own profile.
        Should be redirected.
        """
        response = self.client.get(reverse('action:profile'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_view_profile_edit(self):
        """
        Authenticated users should be able to access this page.
        """
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:profile'))
        self.assertEqual(response.status_code, 200)
