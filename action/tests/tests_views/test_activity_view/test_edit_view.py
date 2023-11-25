from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from django.contrib.messages import get_messages
from action.tests.utils import create_activity, create_user, USER_DATA_1, USER_DATA_2


class ActivityEditViewTests(TestCase):
    def setUp(self) -> None:
        self.user_1 = create_user(**USER_DATA_1)
        self.user_2 = create_user(**USER_DATA_2)

        self.activity_1 = create_activity(self.user_1)
        self.activity_2 = create_activity(self.user_2)

    def test_edit_activity_as_guest(self):
        """
        Unauthenticated users are not allowed to access this function.
        Should be redirected to the index page.
        """
        url = reverse('action:edit', args=(self.activity_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_edit_activity_as_owner(self):
        """
        Authenticated users are allowed to edit their own activity.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:edit', args=(self.activity_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_others_activity(self):
        """
        Authenticated users are not allowed to edit others' activity.
        Should be redirected and failed messages should be shown.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:edit', args=(self.activity_2.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('action:index'))
        # Check for the failed messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You do not have permission to edit this activity.')

    def test_valid_edit_form_submission(self):
        """
        Should be able to edit the activity by valid form.
        Successful messages should be shown.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:edit', args=(self.activity_1.id,))
        form_data = {
            "owner": self.user_1.pk,
            "title": "Change",
            "pub_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(days=1),
            "start_date": timezone.now() + timezone.timedelta(days=2),
            "last_date": timezone.now() + timezone.timedelta(days=3),
            "description": "testdesc",
            "place": "testplace",
            "full_description": "testfulldesc",
        }
        response = self.client.post(url, data=form_data)
        self.assertRedirects(response, reverse('action:manage'))
        # # Check the success messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Activity edited successfully.')

    def test_invalid_edit_form_submission(self):
        """
        Should not be able to edit the activity by invalid form.
        Failed messages should be shown.
        """
        self.client.force_login(self.user_1)
        url = reverse('action:edit', args=(self.activity_1.id,))
        form_data = {
            "title": "",
            "pub_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(days=1),
            "start_date": timezone.now() + timezone.timedelta(days=2),
            "last_date": timezone.now() + timezone.timedelta(days=3),
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)
        # Check the success messages.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Activity edit failed. Please check the form.")
