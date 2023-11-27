from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_user, USER_DATA_1
from django.contrib.messages import get_messages
from action.views import ProfileEditView


class ProfileEditViewTests(TestCase):
    """Test edit user profile view."""

    def setUp(self) -> None:
        """Set up user instance."""
        self.user_1 = create_user(**USER_DATA_1)

    def test_guest_view_profile_edit(self):
        """Test that guests cannot edit their own profiles and are redirected."""
        response = self.client.get(reverse('action:profile'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_view_profile_edit(self):
        """Test that authenticated users can access the profile edit page."""
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('action:profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_valid_form_submission(self):
        """
        Test that users can edit their profiles if the form is valid, and successful messages are shown.

        1. Log in as a user.
        2. Send a POST request to the profile edit page with valid form data.
        3. Assert that the response is redirected to the profile page.
        4. Check that a success message about profile editing is present.
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
        Test that users cannot edit their profiles if the form is invalid, and failed messages are shown.

        1. Log in as a user.
        2. Send a POST request to the profile edit page with invalid form data.
        3. Assert that the response status code is 200 (OK).
        4. Check that a failure message about invalid form data is present.
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
        Test the redirection after a successful edit, which should redirect to the profile page.

        1. Instantiate the `EditProfileView` class.
        2. Get the success URL.
        3. Assert that the success URL is the reverse of the profile page.
        """
        view = ProfileEditView()
        success_url = view.get_success_url()
        self.assertEqual(success_url, reverse('action:profile'))
