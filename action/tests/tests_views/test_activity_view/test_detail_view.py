import time

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.contrib.messages import get_messages

from action.models import ActivityStatus
from action.tests.end_to_end_base import EndToEndTestBase
from action.tests.utils import create_user, create_activity


class ActivityDetailViewTests(TestCase):
    def setUp(self) -> None:
        user_data = {"email": "test@example.com"}
        self.user = create_user(username="John", password="abc", **user_data)
        self.activity = create_activity(self.user)

    def test_view_activity_detail_guest(self):
        """
        Anyone should be able to view the detail of any existent activity.
        """
        url = reverse('action:detail', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn('activity', response.context)
        self.assertEqual(response.context['activity'], self.activity)

    def test_view_activity_detail_upcoming(self):
        """
        Anyone should be able to view the detail of any existent activity.
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
        Authenticated users should be able to view
        the detail of any available activity.
        """
        self.client.force_login(self.user)
        url = reverse('action:detail', args=(self.activity.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn('activity', response.context)
        self.assertEqual(response.context['activity'], self.activity)

    def test_view_nonexistent_activity_detail(self):
        """
        Should not be able to view the details of nonexistent activity.
        Should be redirected to index instead.
        Failed messages should be shown.
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


class ActivityDetailViewTestsE2E(EndToEndTestBase):
    def setUp(self):
        super().setUp()

        self.user = create_user(username='user1', password='pass1')
        self.login(username='user1', password='pass1')
        self.activity = create_activity(self.user)
        self.view = 'action:detail'

    def open_activity(self, activity):
        self.url = self.getUrl(self.view, (activity.id,))
        self.browser.get(self.url)

    def participated_count(self):
        return ActivityStatus.objects.filter(
            id__in=self.user.participated_activity).count()

    def find_by_class(self, class_name):
        return self.browser.find_element(self.by.CLASS_NAME, class_name)

    def test_participate(self):
        self.open_activity(self.activity)

        # Ensure user is not participating initially
        self.assertEqual(self.participated_count(), 0)

        # Participate and check button text
        participate_button = self.find_by_class("Participate")
        self.assertEqual(participate_button.text, 'Participate')
        participate_button.click()

        # Check if button text changes after participating
        participate_button = self.find_by_class("Participate")
        self.assertEqual(participate_button.text, 'Leave')

        # Check if user is now participating
        self.assertEqual(self.participated_count(), 1)

        # Leave and check button text
        participate_button.click()
        participate_button = self.find_by_class("Participate")
        self.assertEqual(participate_button.text, 'Participate')

        # Ensure user is no longer participating
        self.assertEqual(self.participated_count(), 0)

    def test_unable_to_participate_upcoming_activity(self):
        future_date = {
            "pub_date": timezone.now() + timezone.timedelta(days=3),
            "end_date": timezone.now() + timezone.timedelta(days=4),
            "start_date": timezone.now() + timezone.timedelta(days=5),
            "last_date": timezone.now() + timezone.timedelta(days=6)
        }
        future_activity = create_activity(self.user, **future_date)
        self.open_activity(future_activity)

        participate_button = self.find_by_class("Participate")
        participate_button.click()

        # Check the messages.
        messages = self.find_by_class("alert-msg")
        except_text = 'Registration for the activity has not yet opened.'
        self.assertIn(except_text, messages.text)
