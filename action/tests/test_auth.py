"""Tests of authentication."""
from django.urls import reverse
from django.test import TestCase
from mysite import settings
from action.tests import utils


class UserAuthTest(TestCase):
    """Tests user authentication."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Create a social app.
        2. Create a user.
        3. Create an activity with the user.
        """
        self.social_app = utils.create_social_app()
        self.username = "testuser"
        self.password = "testpass"
        self.user = utils.create_user(self.username, self.password)
        self.activity = utils.create_activity(self.user)

    def test_logout(self):
        """
        Test user logout functionality.

        1. Log in the user.
        2. Visit the logout URL.
        3. Assert that the response status code is 302 (redirect).
        4. Assert that the response redirects to the logout redirect URL.
        """
        self.assertTrue(
            self.client.login(username=self.username, password=self.password)
        )
        logout_url = reverse("logout")
        response = self.client.post(logout_url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_login_view(self):
        """
        Test user login through the login view.

        1. Visit the login URL.
        2. Assert that the response status code is 200.
        3. Provide valid login form data.
        4. Assert that the response status code is 302 (redirect).
        5. Assert that the response redirects to the login redirect URL.
        """
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
        """
        Test authentication requirement for participation.

        1. Visit the participate URL for an activity.
        2. Assert that the response status code is 302 (redirect).
        3. Assert that the response redirects to the login URL with the participate URL as the next parameter.
        """
        participate_url = reverse('action:participate',
                                  args=[self.activity.id])
        response = self.client.post(participate_url)
        self.assertEqual(response.status_code, 302)
        login_with_next = f"{reverse('login')}?next={participate_url}"
        self.assertRedirects(response, login_with_next)

    def test_login_with_nonexistent_username(self):
        """
        Test login with a nonexistent username.

        1. Visit the login URL.
        2. Provide form data with a nonexistent username and an unknown password.
        3. Assert that the response status code is 200.
        4. Assert that the response contains a message about entering correct username and password.
        """
        login_url = reverse("login")
        form_data = {"username": "nonexistent", "password": "UnknownPassword"}
        response = self.client.post(login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Please enter a correct username and password.")

    def test_login_with_invalid_password(self):
        """
        Test login with an invalid password.

        1. Visit the login URL.
        2. Provide form data with a valid username and an invalid password.
        3. Assert that the response status code is 200.
        4. Assert that the response contains a message about entering correct username and password.
        """
        login_url = reverse("login")
        form_data = {"username": self.username, "password": "InvalidPassword"}
        response = self.client.post(login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Please enter a correct username and password.")
