from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages

from action.tests.end_to_end_base import EndToEndTestBase
from action.tests.utils import create_activity, create_user, USER_DATA_1, USER_DATA_2
from action.models import Activity


class ActivityDeleteViewTests(TestCase):
    """Test cases for the ActivityDeleteView."""

    def setUp(self):
        """Set up the test environment by creating test users and activities."""
        self.user_1 = create_user(**USER_DATA_1)
        self.user_2 = create_user(**USER_DATA_2)

        self.activity_1 = create_activity(self.user_1)
        self.activity_2 = create_activity(self.user_2)

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
        self.assertEqual(str(messages[0]), "You do not have permission to delete this activity.")
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
        self.assertRedirects(response, reverse('action:index'))
        # Check for the failed messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Activity doesn't exist.")


class DeleteActivityTestsE2E(EndToEndTestBase):
    """Test case for the views related to activity deletion."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Define a username and password.
        2. Create a user with the defined username and password.
        """
        super().setUp()
        self.name_1 = 'user1'
        self.password_1 = 'pass1'
        self.user_1 = create_user(self.name_1, self.password_1)

    def test_delete_activity(self):
        """
        Test delete an activity.

        1. Create a new activity.
        2. Check the initial activity amount.
        3. LogIn.
        4. Navigate to activity manage page.
        5. Delete the activity.
        6. Check the messages.
        7. Check that the activity was deleted.
        """
        # Create an activity
        create_activity(self.user_1)

        # Check the activity amount
        initial_count = Activity.objects.filter(owner=self.user_1)
        self.assertEqual(len(initial_count), 1)

        # LogIn as user_1
        self.login(self.name_1, self.password_1)

        # Navigate to activity manage page
        url = self.getUrl("action:manage")
        self.browser.get(url)

        # Delete the activity
        delete_button = self.find_by_class("activity-delete")
        delete_button.click()

        # Check the messages
        message = self.find_by_class("alert-msg")
        self.assertIn("You have successfully deleted this activity.", message.text)

        # Check that the activity was deleted.
        activity = Activity.objects.filter(owner=self.user_1)
        self.assertEqual(len(activity), 0)
