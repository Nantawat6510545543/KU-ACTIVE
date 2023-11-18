from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user
from django.contrib.messages import get_messages
from action.views import EditProfileView


class ProfileEditViewTests(TestCase):
    def setUp(self) -> None:
        user_data_1 = {"email": "test1@example.com"}
        self.user_1 = create_user(username="John", password="abc", **user_data_1)

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

    def test_edit_profile_valid_form_submission(self):
        """
        Should be able to edit profile if the form is valid.
        Successful messages should be shown.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:edit_profile')
        form_data = {'username': 'test1'}
        response = self.client.post(url, data=form_data)
        # Check the redirection.
        self.assertRedirects(response, reverse('action:profile'))
        # Check the success messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Profile edited successfully.')

    def test_edit_profile_invalid_form_submission(self):
        """
        Should not be able to edit profile if the form is invalid.
        Failed messages should be shown.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:edit_profile')
        form_data = {'username': ''}
        response = self.client.post(url, data=form_data)
        # Check the redirection, Should not be redirected.
        self.assertEqual(response.status_code, 200)
        # Check the success messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Profile edit failed. Please check the form.')

    def test_edit_profile_get_success_url(self):
        """
        Tests the redirection.
        Should redirect the successful action to profile page.
        """
        view = EditProfileView()
        success_url = view.get_success_url()
        self.assertEqual(success_url, reverse('action:profile'))
