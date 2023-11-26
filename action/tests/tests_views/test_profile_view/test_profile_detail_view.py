from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user, USER_DATA_1, USER_DATA_2
from django.contrib.messages import get_messages


class ProfileDetailViewTests(TestCase):
    """Test user profile detail view."""

    def setUp(self) -> None:
        """Set up two user instances."""
        self.user_1 = create_user(**USER_DATA_1)
        self.user_2 = create_user(**USER_DATA_2)

    def test_guest_view_profile(self):
        """Test that guests cannot view their own profiles and are redirected to the login page."""
        response = self.client.get(reverse('action:profile'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_view_profile(self):
        """Test that authenticated users can view their own profiles."""
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:profile'))
        self.assertEqual(response.status_code, 200)

    def test_guest_view_others_profile(self):
        """Test that guests cannot view other users' profiles and are redirected."""
        response = self.client.get(reverse('action:profile'), args=(self.user_2.id,))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_view_others_profile(self):
        """
        Test that authenticated users can view other users' profiles.

        1. Log in as a user.
        2. Send a GET request to another user's profile page.
        3. Assert that the response status code is 200 (OK).
        """
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:profile'), args=(self.user_2.id,))
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.user_2)
        response = self.client.get(reverse('action:profile'), args=(self.user_1.id,))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_view_own_profile(self):
        """
        Test that authenticated users can view their own profiles.

        1. Log in as a user.
        2. Send a GET request to the own profile page.
        3. Assert that the response status code is 200 (OK).
        """
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:profile'), args=(self.user_1.id,))
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.user_2)
        response = self.client.get(reverse('action:profile'), args=(self.user_2.id,))
        self.assertEqual(response.status_code, 200)

    def test_profile_not_exists(self):
        """
        Test that anyone should not be able to check an unavailable profile, and failed messages should be shown.

        1. Log in as a user.
        2. Send a GET request to an invalid user's profile page.
        3. Assert that the response is redirected to the index page.
        4. Check that a failure message about an invalid user ID is present.
        """
        invalid_user_id = 999
        self.client.force_login(self.user_1)
        url = reverse('action:profile', kwargs={'user_id': invalid_user_id})
        response = self.client.get(url)
        # Check redirection.
        self.assertRedirects(response, reverse('action:index'))

        # Check messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid user id.")
