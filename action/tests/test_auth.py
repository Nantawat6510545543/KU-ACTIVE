"""Tests of authentication."""
from django.urls import reverse
from mysite import settings
from .utils import Tester


class UserAuthTest(Tester):
    """
    Tests user authentication.
    """

    def setUp(self):
        super().setUp()
        self.username = "testuser"
        self.password = "testpass"
        self.user = self.create_user(self.username, self.password)
        self.activity = self.create_activity(self.user)

    def test_logout(self):
        """A user can log out using the logout url.

        As an authenticated user,
        when I visit /accounts/logout/
        then I am logged out
        and then redirected to the login page.
        """
        logout_url = reverse("logout")
        self.assertTrue(
            self.client.login(username=self.username, password=self.password)
        )
        response = self.client.get(logout_url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_login_view(self):
        """A user can log in using the login view."""
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        form_data = {"username": "testuser",
                     "password": "testpass"
                     }
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_auth_required_to_participation(self):
        """Authentication is required to submit a vote.

        As an unauthenticated user,
        when I submit a vote for a question,
        then I am redirected to the login page,
        or I receive a 403 response (FORBIDDEN)
        """
        participate_url = reverse('action:participate',
                                  args=[self.activity.id])
        response = self.client.post(participate_url)
        self.assertEqual(response.status_code, 302)
        login_with_next = f"{reverse('login')}?next={participate_url}"
        self.assertRedirects(response, login_with_next)

    def test_login_with_nonexistent_username(self):
        """
        Make sure a user cannot log in using a username that doesn't exist.
        """
        login_url = reverse("login")
        form_data = {"username": "nonexistent", "password": "UnknownPassword"}
        response = self.client.post(login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Please enter a correct username and password.")

    def test_login_with_invalid_password(self):
        """
        Make sure a user cannot log in with an invalid password.
        """
        login_url = reverse("login")
        form_data = {"username": self.username, "password": "InvalidPassword"}
        response = self.client.post(login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Please enter a correct username and password.")
