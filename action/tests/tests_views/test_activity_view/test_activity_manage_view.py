from django.urls import reverse
from django.test import TestCase
from action.tests.utils import create_activity, create_user, USER_DATA_1, USER_DATA_2


class ActivityManageViewTests(TestCase):
    """Test cases for the ActivityManageView."""

    def setUp(self):
        """Set up the test environment by creating test users and activities."""
        self.user_1 = create_user(**USER_DATA_1)
        self.user_2 = create_user(**USER_DATA_2)

        self.activity_1 = create_activity(self.user_1)
        self.activity_2 = create_activity(self.user_2)

    def test_manage_activity_guest(self):
        """
        Test whether guests have permission to access the activity management view.

        Guests should be redirected to the login page.
        """
        url = reverse('action:manage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_manage_activity_authenticated(self):
        """
        Test whether authenticated users have permission to access the activity management view.

        Authenticated users should be able to access the view with a status code of 200.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:manage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
