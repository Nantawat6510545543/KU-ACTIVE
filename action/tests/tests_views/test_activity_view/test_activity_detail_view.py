from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.contrib.messages import get_messages

from action.tests.utils import create_user, create_activity, USER_DATA_1


class ActivityDetailViewTests(TestCase):
    """Test case for the views related to activity details."""

    def setUp(self):
        """
        Set up common attributes for the test methods.

        1. Create a user.
        2. Create an activity with the user.
        """
        self.user = create_user(**USER_DATA_1)
        self.activity = create_activity(self.user)

    def test_view_activity_detail_guest(self):
        """
        Test the activity detail view for a guest user.

        1. Attempt to view the detail of an existing activity.
        2. Assert that the response status code is 200.
        3. Assert that the 'activity' key is present in the context.
        4. Assert that the 'activity' in the context matches the created activity.
        """
        url = reverse('action:detail', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn('activity', response.context)
        self.assertEqual(response.context['activity'], self.activity)

    def test_view_activity_detail_upcoming(self):
        """
        Test the activity detail view for an upcoming activity.

        1. Create an upcoming activity.
        2. Attempt to view the detail of the upcoming activity.
        3. Assert that the response status code is 200.
        4. Assert that the 'activity' key is present in the context.
        5. Assert that the 'activity' in the context matches the created upcoming activity.
        """
        future_date = {
            "pub_date": timezone.now() + timezone.timedelta(days=3),
            "end_date": timezone.now() + timezone.timedelta(days=4),
            "start_date": timezone.now() + timezone.timedelta(days=5),
            "last_date": timezone.now() + timezone.timedelta(days=6)
        }
        future_activity = create_activity(self.user, **future_date)
        url = reverse('action:detail', args=(future_activity.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('activity', response.context)
        self.assertEqual(response.context['activity'], future_activity)

    def test_view_activity_detail_authenticated(self):
        """
        Test the activity detail view for an authenticated user.

        1. Log in the user.
        2. Attempt to view the detail of an existing activity.
        3. Assert that the response status code is 200.
        4. Assert that the 'activity' key is present in the context.
        5. Assert that the 'activity' in the context matches the created activity.
        """
        self.client.force_login(self.user)
        url = reverse('action:detail', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn('activity', response.context)
        self.assertEqual(response.context['activity'], self.activity)

    def test_view_nonexistent_activity_detail(self):
        """
        Test attempting to view details of a nonexistent activity.

        1. Attempt to view the detail of a nonexistent activity.
        2. Assert that the response status code is 302 (redirect).
        3. Assert that the response redirects to the index page.
        4. Assert that a message indicating that the activity does not exist is present.
        """
        nonexistent_act_id = 999
        url = reverse('action:detail', args=(nonexistent_act_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('action:index'))
        # Check the messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Activity does not exist.')
