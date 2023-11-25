from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages
from action.tests.utils import create_activity, create_user, USER_DATA_1, USER_DATA_2
from action.models import Activity


class ActivityManageViewTests(TestCase):
    def setUp(self) -> None:
        self.user_1 = create_user(**USER_DATA_1)
        self.user_2 = create_user(**USER_DATA_2)

        self.activity_1 = create_activity(self.user_1)
        self.activity_2 = create_activity(self.user_2)

    def test_manage_activity_guest(self):
        """
        Guest should not have a permission to access this page.
        Should be redirected.
        """
        url = reverse('action:manage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_manage_activity_authenticated(self):
        """
        Authenticated users should have a permission to access this page.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:manage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_activity_as_guest(self):
        """
        Guest should not have permission to access this feature.
        Should be redirected.
        """
        url = reverse('action:delete_activity', args=(self.activity_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_activity_as_owner(self):
        """
        Authenticated users should be able to delete their own activity.
        Successful message should be shown.
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
        Anyone should not be able to delete others' activity.
        Failed message should be shown.
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
        Anyone should not be able to delete nonexistent activity.
        Failed message should be shown.
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
