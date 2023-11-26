from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages
from action.tests.utils import create_activity, create_user, USER_DATA_1, USER_DATA_2
from action.models import Activity


class ActivityManageViewTests(TestCase):
    """Test cases for the ActivityManageView."""

    def setUp(self) -> None:
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

    def test_delete_activity_as_guest(self):
        """
        Test whether guests have permission to delete an activity.

        Guests should be redirected when attempting to delete an activity.
        """
        url = reverse('action:delete_activity', args=(self.activity_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_activity_as_owner(self):
        """
        Test whether authenticated owners can successfully delete their own activity.

        Authenticated owners should be redirected to the activity management view with a success message.
        The activity should be deleted from the database.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:delete_activity', args=(self.activity_1.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('action:manage'))
        # Check for the success messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have successfully deleted this activity.")
        # Check that the activity is deleted.
        with self.assertRaises(Activity.DoesNotExist):
            Activity.objects.get(id=self.activity_1.pk)

    def test_delete_others_activity(self):
        """
        Test whether users can delete activities owned by others.

        Users attempting to delete others' activities should be redirected with a failed message.
        The target activity should remain in the database.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:delete_activity', args=(self.activity_2.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('action:manage'))
        # Check for the failed messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to delete this activity")
        # Check that the activity has not yet been deleted.
        self.assertEqual(Activity.objects.get(id=self.activity_2.pk).owner, self.user_2)

    def test_delete_nonexistent_activity(self):
        """
        Test whether users can delete a nonexistent activity.

        Users attempting to delete a nonexistent activity should be redirected with a failed message.
        """
        nonexistent_activity_id = 999
        self.client.force_login(self.user_1)
        url = reverse('action:delete_activity', args=(nonexistent_activity_id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('action:manage'))
        # Check for the failed messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Activity doesn't exist")
