from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages

from action.models import ActivityStatus
from action.tests.utils import create_user, create_activity, \
    create_activity_status, USER_DATA_1, USER_DATA_2


class FavoriteViewTests(TestCase):
    def setUp(self):
        """Set up the test environment by creating test users, activities, and a social app."""
        self.user_1 = create_user(**USER_DATA_1)
        self.user_2 = create_user(**USER_DATA_2)

        self.activity_1 = create_activity(self.user_1)
        self.activity_2 = create_activity(self.user_2)

    def test_activity_favorite_as_owner(self):
        """
        Test whether authenticated owners can favorite their available activity.

        Authenticated owners should be redirected to the activity detail page with a success message.
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
        Test whether authenticated users can favorite others' available activity.

        Authenticated users should be redirected to the activity detail page with a success message.
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
        Test whether authenticated users cannot favorite an activity they have already favorited.

        Authenticated users should be redirected to the activity detail page with a failed message.
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
