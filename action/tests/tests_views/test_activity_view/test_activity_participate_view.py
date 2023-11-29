from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.contrib.messages import get_messages

from action.models import ActivityStatus
from action.tests.utils import create_user, create_activity, \
    create_activity_status, create_social_app, USER_DATA_1, USER_DATA_2


class ParticipateViewTests(TestCase):
    """Test cases for the ActivityStatusView."""

    def setUp(self):
        """Set up the test environment by creating test users, activities, and a social app."""
        self.user_1 = create_user(**USER_DATA_1)
        self.user_2 = create_user(**USER_DATA_2)

        self.activity_1 = create_activity(self.user_1)
        self.activity_2 = create_activity(self.user_2)
        self.social_app = create_social_app()

    def test_activity_participation_as_owner(self):
        """
        Test whether authenticated owners can participate in their available activity.

        Authenticated owners should be redirected to the activity detail page with a success message.
        """
        create_activity_status(self.user_1, self.activity_1, is_participated=False)
        self.client.force_login(self.user_1)
        url = reverse('action:participate', args=(self.activity_1.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_1.id,)))
        # Check for successful messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have successfully participated.")
        # Check that the activity status is updated.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_1)
        self.assertTrue(updated_activity_status.is_participated)

    def test_activity_participation_others(self):
        """
        Test whether authenticated users can participate in others' available activity.

        Authenticated users should be redirected to the activity detail page with a success message.
        """
        create_activity_status(self.user_1, self.activity_2, is_participated=False)
        self.client.force_login(self.user_1)
        url = reverse('action:participate', args=(self.activity_2.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_2.id,)))
        # Check for successful messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have successfully participated.")
        # Check that the activity status is updated.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_2)
        self.assertTrue(updated_activity_status.is_participated)

    def test_activity_participation_already_participating(self):
        """
        Test whether authenticated users cannot participate in an activity they are already participating in.

        Authenticated users should be redirected to the activity detail page with a failed message.
        """
        create_activity_status(self.user_1, self.activity_1, is_participated=True)
        self.client.force_login(self.user_1)
        url = reverse('action:participate', args=(self.activity_1.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_1.id,)))
        # Check for failed messages.
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are already participating.")
        # Check that the activity status is remained the same.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_1)
        self.assertTrue(updated_activity_status.is_participated)

    def test_unavailable_activity_participation(self):
        """
        Test whether anyone can participate in an unavailable activity.

        Anyone attempting to participate in an unavailable activity should be redirected with a failed message.
        """
        form_data = {
            "title": "Test",
            "pub_date": timezone.now(),
            "end_date": timezone.now(),
            "start_date": timezone.now() + timezone.timedelta(days=5),
            "last_date": timezone.now() + timezone.timedelta(days=6),
        }
        unavailable_activity = create_activity(self.user_2, **form_data)

        create_activity_status(self.user_1, unavailable_activity, is_participated=False)
        self.client.force_login(self.user_1)

        url = reverse('action:participate', args=(unavailable_activity.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(unavailable_activity.id,)))
        # Check for failed messages.
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This activity can no longer be participated in.")
        # Check that the activity status is remained the same.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=unavailable_activity)
        self.assertFalse(updated_activity_status.is_participated)
