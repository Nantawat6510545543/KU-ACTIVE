from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.contrib.messages import get_messages

from action.models import ActivityStatus
from action.tests.utils import create_user, create_activity, create_activity_status, create_social_app


class ActivityStatusViewTests(TestCase):
    def setUp(self) -> None:
        user_data_1 = {"email": "test1@example.com"}
        user_data_2 = {"email": "test2@example.com"}
        self.user_1 = create_user(username="John", password="abc", **user_data_1)
        self.user_2 = create_user(username="Jane", password="abc", **user_data_2)
        self.activity_1 = create_activity(self.user_1)
        self.activity_2 = create_activity(self.user_2)
        self.social_app = create_social_app()

    def test_activity_participation_as_owner(self):
        """
        Authenticated users should be able to participate in their available activity.
        Successful messages should be shown.
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
        Authenticated users should be able to participate in others' available activity.
        Successful messages should be shown.
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
        Authenticated users should not be able to participate in any activity
        that they are already participating in.
        Failed messages should be shown.
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
        Anyone should not be able to participate in any unavailable activity.
        Failed messages should be shown.
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

    def test_activity_leave(self):
        """
        Authenticated users should be able to leave activities
        in which they have participated.
        Successful messages should be shown.
        """
        create_activity_status(self.user_1, self.activity_1, is_participated=True)
        self.client.force_login(self.user_1)
        url = reverse('action:leave', args=(self.activity_1.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_1.id,)))
        # Check for successful messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have left this activity.")
        # Check that the activity status is updated.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_1)
        self.assertFalse(updated_activity_status.is_participated)

    def test_activity_leave_not_partipate(self):
        """
        Authenticated users should not be able to leave activities
        in which they have not yet participated.
        Failed messages should be shown.
        """
        create_activity_status(self.user_1, self.activity_1, is_participated=False)
        self.client.force_login(self.user_1)
        url = reverse('action:leave', args=(self.activity_1.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_1.id,)))
        # Check for failed messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are not currently participating in this activity.")
        # Check that the activity status is remained the same.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_1)
        self.assertFalse(updated_activity_status.is_participated)

    def test_activity_favorite_as_owner(self):
        """
        Authenticated users should be able to favorite their available activity.
        Successful messages should be shown.
        """
        create_activity_status(self.user_1, self.activity_1)
        self.client.force_login(self.user_1)
        url = reverse('action:favorite', args=(self.activity_1.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_1.id,)))
        # Check for successful messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have successfully favorited this activity.")
        # Check that the activity status is updated.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_1)
        self.assertTrue(updated_activity_status.is_favorited)

    def test_activity_favorite_others(self):
        """
        Authenticated users should be able to favorite others' available activity.
        Successful messages should be shown.
        """
        create_activity_status(self.user_1, self.activity_2)
        self.client.force_login(self.user_1)
        url = reverse('action:favorite', args=(self.activity_2.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_2.id,)))
        # Check for successful messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have successfully favorited this activity.")
        # Check that the activity status is updated.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_2)
        self.assertTrue(updated_activity_status.is_favorited)

    def test_activity_favorite_already_favorite(self):
        """
        Authenticated users should not be able to favorite any activity
        that they are already favorite.
        Failed messages should be shown.
        """
        create_activity_status(self.user_1, self.activity_1, is_favorited=True)
        self.client.force_login(self.user_1)
        url = reverse('action:favorite', args=(self.activity_1.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_1.id,)))
        # Check for failed messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have already favorited this activity.")
        # Check that the activity status is remained the same.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_1)
        self.assertTrue(updated_activity_status.is_favorited)

    def test_activity_unfavorite(self):
        """
        Authenticated users should be able to unfavorite the activity.
        Successful messages should be shown.
        """
        create_activity_status(self.user_1, self.activity_1, is_favorited=True)
        self.client.force_login(self.user_1)
        url = reverse('action:unfavorite', args=(self.activity_1.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_1.id,)))
        # Check for successful messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have unfavorited this activity.")
        # Check that the activity status is updated.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_1)
        self.assertFalse(updated_activity_status.is_favorited)

    def test_activity_unfavorite_not_yet_favorited(self):
        """
        Authenticated users should not be able to unfavorite an activity
        that they have not favorited.
        Failed messages should be shown.
        """
        create_activity_status(self.user_1, self.activity_1, is_favorited=False)
        self.client.force_login(self.user_1)
        url = reverse('action:unfavorite', args=(self.activity_1.id,))
        response = self.client.get(url)
        # Check that the user was redirected to the detail page.
        self.assertRedirects(response, reverse('action:detail', args=(self.activity_1.id,)))
        # Check for failed messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have not currently favorite this activity.")
        # Check that the activity status is remained the same.
        updated_activity_status = ActivityStatus.objects.get(participants=self.user_1,
                                                             activity=self.activity_1)
        self.assertFalse(updated_activity_status.is_favorited)
